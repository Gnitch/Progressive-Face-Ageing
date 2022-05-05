import os
import torch
from collections import OrderedDict
from trained_models.cyclegan.models import networks


class BaseModel():

    # modify parser to add command line options,
    # and also change the default values if needed
    @staticmethod
    def modify_commandline_options(parser, is_train):
        return parser

    def name(self):
        return 'BaseModel'

    def initialize(self, opt):
        self.opt = opt
        self.gpu_ids = opt.gpu_ids
        self.isTrain = opt.isTrain
        self.device = torch.device('cuda:{}'.format(self.gpu_ids[0])) if self.gpu_ids else torch.device('cpu')
        self.save_dir = os.path.join(opt.checkpoints_dir, opt.name)
        if opt.resize_or_crop != 'scale_width':
            torch.backends.cudnn.benchmark = True
        self.loss_names = []
        self.model_names = []
        self.visual_names = []
        self.image_paths = []
        self.G_A_freeze_layer = opt.G_A_freeze_layer
        self.G_B_freeze_layer = opt.G_B_freeze_layer
        self.D_A_freeze_layer = opt.D_A_freeze_layer
        self.D_B_freeze_layer = opt.D_B_freeze_layer
        self.use_pretrained_model = opt.use_pretrained_model
        self.pretrained_model_name = opt.pretrained_model_name
        self.pretrained_model_subname = opt.pretrained_model_subname
        self.pretrained_model_epoch = opt.pretrained_model_epoch
        self.pretrained_save_dir = os.path.join(opt.checkpoints_dir, opt.pretrained_model_name)

    def set_input(self, input):
        self.input = input

    def forward(self):
        pass

    # load and print networks; create schedulers
    def setup(self, opt, parser=None):
        if self.isTrain:
            self.schedulers = [networks.get_scheduler(optimizer, opt) for optimizer in self.optimizers]

        if not self.isTrain or opt.continue_train:
            self.load_networks(opt.epoch)
        if self.isTrain and opt.use_pretrained_model:
            self.load_pretrained_networks(opt.pretrained_model_epoch)
        self.print_networks(opt.verbose)

    # make models eval mode during test time
    def eval(self):
        for name in self.model_names:
            if isinstance(name, str):
                net = getattr(self, 'net' + name)
                net.eval()

    # used in test time, wrapping `forward` in no_grad() so we don't save
    # intermediate steps for backprop
    def test(self):
        with torch.no_grad():
            self.forward()

    # get image paths
    def get_image_paths(self):
        return self.image_paths

    def optimize_parameters(self):
        pass

    # update learning rate (called once every epoch)
    def update_learning_rate(self):
        for scheduler in self.schedulers:
            scheduler.step()
        lr = self.optimizers[0].param_groups[0]['lr']
        # print('learning rate = %.7f' % lr)

    # return visualization images. train.py will display these images, and save the images to a html
    def get_current_visuals(self):
        visual_ret = OrderedDict()
        print(self.visual_names)
        for name in self.visual_names:
            if isinstance(name, str):
                visual_ret[name] = getattr(self, name)
        return visual_ret

    # return traning losses/errors. train.py will print out these errors as debugging information
    def get_current_losses(self):
        errors_ret = OrderedDict()
        for name in self.loss_names:
            if isinstance(name, str):
                # float(...) works for both scalar tensor and float number
                errors_ret[name] = float(getattr(self, 'loss_' + name))
        return errors_ret

    # save models to the disk
    def save_networks(self, epoch):
        for name in self.model_names:
            if isinstance(name, str):
                save_filename = '%s_net_%s.pth' % (epoch, name)
                save_path = os.path.join(self.save_dir, save_filename)
                net = getattr(self, 'net' + name)

                if len(self.gpu_ids) > 0 and torch.cuda.is_available():
                    torch.save(net.module.cpu().state_dict(), save_path)
                    net.cuda(self.gpu_ids[0])
                else:
                    torch.save(net.cpu().state_dict(), save_path)

    def __patch_instance_norm_state_dict(self, state_dict, module, keys, i=0):
        key = keys[i]
        if i + 1 == len(keys):  # at the end, pointing to a parameter/buffer
            if module.__class__.__name__.startswith('InstanceNorm') and \
                    (key == 'running_mean' or key == 'running_var'):
                if getattr(module, key) is None:
                    state_dict.pop('.'.join(keys))
            if module.__class__.__name__.startswith('InstanceNorm') and \
               (key == 'num_batches_tracked'):
                state_dict.pop('.'.join(keys))
        else:
            self.__patch_instance_norm_state_dict(state_dict, getattr(module, key), keys, i + 1)

    # load models from the disk
    def load_networks(self, epoch):
        for name in self.model_names:
            if isinstance(name, str):
                load_filename = '%s_net_%s.pth' % (epoch, name)
                load_path = os.path.join(self.save_dir, load_filename)
                net = getattr(self, 'net' + name)
                if isinstance(net, torch.nn.DataParallel):
                    net = net.module
                # print('loading the model from %s' % load_path)
                # if you are using PyTorch newer than 0.4 (e.g., built from
                # GitHub source), you can remove str() on self.device
                state_dict = torch.load(load_path, map_location=str(self.device))
                if hasattr(state_dict, '_metadata'):
                    del state_dict._metadata

                # patch InstanceNorm checkpoints prior to 0.4
                for key in list(state_dict.keys()):  # need to copy keys here because we mutate in loop
                    self.__patch_instance_norm_state_dict(state_dict, net, key.split('.'))
                net.load_state_dict(state_dict)

    # load models from the disk
    def load_pretrained_networks(self, epoch):
        for name in self.pretrained_model_subname.split(','):
            if isinstance(name, str):
                load_filename = 'latest_net_%s.pth' % (name)
                load_path = os.path.join(
                    "trained_model", load_filename)
                
                net = getattr(self, 'net' + name)
                if isinstance(net, torch.nn.DataParallel):
                    net = net.module
                load_path = "trained_model/1_wiki_base_mix/latest_net_%s.pth" % (name)
                # print('loading the model from %s' % load_path)
                # if you are using PyTorch newer than 0.4 (e.g., built from
                # GitHub source), you can remove str() on self.device                
                state_dict = torch.load(
                    load_path, map_location=str(self.device))
                if hasattr(state_dict, '_metadata'):
                    del state_dict._metadata

                # patch InstanceNorm checkpoints prior to 0.4
                # need to copy keys here because we mutate in loop
                for key in list(state_dict.keys()):
                    self.__patch_instance_norm_state_dict(
                        state_dict, net, key.split('.'))
                net.load_state_dict(state_dict)

    # print network information
    def print_networks(self, verbose):
        # print('---------- Networks initialized -------------')
        # for name in self.model_names:
        #     if isinstance(name, str):
        #         net = getattr(self, 'net' + name)
        #         num_params = 0
        #         num_params_trainable = 0
        #         for param in net.parameters():
        #             num_params += param.numel()
        #             if param.requires_grad:
        #                 num_params_trainable += param.numel()
        #         if verbose:
        #             print(net)
        #         print('[Network %s] Total number of parameters : %.3f M' % (name, num_params / 1e6))
        #         print('[Network %s] Total number of trainable parameters : %.3f M' % (name, num_params_trainable / 1e6))
        # print('-----------------------------------------------')
        pass

    # set requies_grad=Fasle to avoid computation
    def set_requires_grad(self, nets, requires_grad=False):
        if not isinstance(nets, list):
            nets = [nets]
        for net in nets:
            if net is not None:
                for param in net.parameters():
                    param.requires_grad = requires_grad
