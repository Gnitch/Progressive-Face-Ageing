import argparse
import os
from trained_models.cyclegan.util import util
import torch
import trained_models.cyclegan.models 
import trained_models.cyclegan.data


class BaseOptions():
    def __init__(self):
        self.initialized = False
        self.model = "cycle_gan"
        self.gpu_ids = []
        self.isTrain = True
        self.checkpoints_dir = "./checkpoints"
        self.name = "experiment_name"
        self.batch_size = 1
        self.loadSize = 286
        self.fineSize = 286
        self.display_winsize = 256
        self.input_nc = 3
        self.output_nc = 3
        self.ngf = 64
        self.ndf = 64
        self.netD = "basic"
        self.netG = "resnet_9blocks"
        self.n_layers_D = 3
        self.dataset_mode = "unaligned"
        self.direction = "AtoB"
        self.epoch = "latest"
        self.num_threads = "4"
        self.norm = "instance"
        self.serial_batches = False
        self.no_dropout = False
        self.max_dataset_size = float("inf")
        self.resize_or_crop = "resize_and_crop"
        self.no_flip = False
        self.init_type = "normal"
        self.init_gain = float(0.02)
        self.verbose = False
        self.suffix = ""

        # Train Options
        self.display_freq = 400
        self.display_ncols = 4
        self.display_id = 1
        self.display_server = "http://localhost"
        self.display_env = "main"
        self.display_port = 8097
        self.update_html_freq = 1000
        self.print_freq = 100
        self.save_latest_freq = 5000
        self.save_epoch_freq = 5
        self.continue_train = False
        self.epoch_count = 1
        self.phase = "train"
        self.use_pretrained_model = False
        self.pretrained_model_name = ""
        self.pretrained_model_subname = ""
        self.pretrained_model_epoch = ""
        self.G_A_freeze_layer = 0
        self.G_B_freeze_layer = 0
        self.D_A_freeze_layer = 0
        self.D_B_freeze_layer = 0
        self.niter = 1
        self.niter_decay = 1
        self.beta1 = 0.5
        self.lr = 0.0002
        self.no_lsgan = False
        self.pool_size = 50
        self.no_html = False
        self.lr_policy = "lambda"
        self.lr_decay_iters = 50
        
    # parser.add_argument('--lambda_A', type=float, default=10.0, help='weight for cycle loss (A -> B -> A)')
    #         parser.add_argument('--lambda_B', type=float, default=10.0,
    #                             help='weight for cycle loss (B -> A -> B)')
    #         parser.add_argument('--lambda_identity', type=float, default=0.5, 

        # cycle_gan_model.py args
        self.lambda_A = 10.0
        self.lambda_B = 10.0
        self.lambda_identity = 0.5


    def initialize(self, parser):
        # parser.add_argument('--dataroot', required=True, help='path to images (should have subfolders trainA, trainB, valA, valB, etc)')
        '''EDITED By Gnitch '''
        parser.add_argument('--dataroot',type=str, default="./datasets/Dataset_Gnitch", help='path to images (should have subfolders trainA, trainB, valA, valB, etc)')

        parser.add_argument('--batch_size', type=int, default=1, help='input batch size')
        parser.add_argument('--loadSize', type=int, default=286, help='scale images to this size')
        parser.add_argument('--fineSize', type=int, default=256, help='then crop to this size')
        parser.add_argument('--display_winsize', type=int, default=256, help='display window size for both visdom and HTML')
        parser.add_argument('--input_nc', type=int, default=3, help='# of input image channels')
        parser.add_argument('--output_nc', type=int, default=3, help='# of output image channels')
        parser.add_argument('--ngf', type=int, default=64, help='# of gen filters in first conv layer')
        parser.add_argument('--ndf', type=int, default=64, help='# of discrim filters in first conv layer')
        parser.add_argument('--netD', type=str, default='basic', help='selects model to use for netD')
        parser.add_argument('--netG', type=str, default='resnet_9blocks', help='selects model to use for netG')
        parser.add_argument('--n_layers_D', type=int, default=3, help='only used if netD==n_layers')
        parser.add_argument('--gpu_ids', type=str, default='0', help='gpu ids: e.g. 0  0,1,2, 0,2. use -1 for CPU')
        parser.add_argument('--name', type=str, default='experiment_name', help='name of the experiment. It decides where to store samples and models')
        parser.add_argument('--dataset_mode', type=str, default='unaligned', help='chooses how datasets are loaded. [unaligned | aligned | single]')
        parser.add_argument('--model', type=str, default='cycle_gan',
                            help='chooses which model to use. cycle_gan, pix2pix, test')
        parser.add_argument('--direction', type=str, default='AtoB', help='AtoB or BtoA')
        parser.add_argument('--epoch', type=str, default='latest', help='which epoch to load? set to latest to use latest cached model')
        parser.add_argument('--num_threads', default=4, type=int, help='# threads for loading data')
        parser.add_argument('--checkpoints_dir', type=str, default='./checkpoints', help='models are saved here')
        parser.add_argument('--norm', type=str, default='instance', help='instance normalization or batch normalization')
        parser.add_argument('--serial_batches', action='store_true', help='if true, takes images in order to make batches, otherwise takes them randomly')
        parser.add_argument('--no_dropout', action='store_true', help='no dropout for the generator')
        parser.add_argument('--max_dataset_size', type=int, default=float("inf"), help='Maximum number of samples allowed per dataset. If the dataset directory contains more than max_dataset_size, only a subset is loaded.')
        parser.add_argument('--resize_or_crop', type=str, default='resize_and_crop', help='scaling and cropping of images at load time [resize_and_crop|crop|scale_width|scale_width_and_crop|none]')
        parser.add_argument('--no_flip', action='store_true', help='if specified, do not flip the images for data augmentation')
        parser.add_argument('--init_type', type=str, default='normal', help='network initialization [normal|xavier|kaiming|orthogonal]')
        parser.add_argument('--init_gain', type=float, default=0.02, help='scaling factor for normal, xavier and orthogonal.')
        parser.add_argument('--verbose', action='store_true', help='if specified, print more debugging information')
        parser.add_argument('--suffix', default='', type=str, help='customized suffix: opt.name = opt.name + suffix: e.g., {model}_{netG}_size{loadSize}')


        
        self.initialized = True
        return parser

    def gather_options(self):
        # initialize parser with basic options
        if not self.initialized:
            parser = argparse.ArgumentParser(
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
            parser = self.initialize(parser)

        # get the basic options
        opt, _ = parser.parse_known_args()

        # modify model-related parser options
        model_name = opt.model
        model_option_setter = trained_models.cyclegan.models.get_option_setter(model_name)
        parser = model_option_setter(parser, self.isTrain)
        opt, _ = parser.parse_known_args()  # parse again with the new defaults

        # modify dataset-related parser options
        dataset_name = opt.dataset_mode
        dataset_option_setter = trained_models.cyclegan.data.get_option_setter(dataset_name)
        parser = dataset_option_setter(parser, self.isTrain)

        self.parser = parser
        return parser.parse_args()

    def print_options(self, opt):
        message = ''
        message += '----------------- Options ---------------\n'
        for k, v in sorted(vars(opt).items()):
            comment = ''
            default = self.parser.get_default(k)
            if v != default:
                comment = '\t[default: %s]' % str(default)
            message += '{:>25}: {:<30}{}\n'.format(str(k), str(v), comment)
        message += '----------------- End -------------------'
        # print(message)

        # save to the disk
        expr_dir = os.path.join(opt.checkpoints_dir, opt.name)
        util.mkdirs(expr_dir)
        file_name = os.path.join(expr_dir, 'opt.txt')
        with open(file_name, 'wt') as opt_file:
            opt_file.write(message)
            opt_file.write('\n')

    def parse(self):

        opt = self.gather_options()
        opt.isTrain = self.isTrain   # train or test

        # process opt.suffix
        if opt.suffix:
            suffix = ('_' + opt.suffix.format(**vars(opt))) if opt.suffix != '' else ''
            opt.name = opt.name + suffix

        # self.print_options(opt)

        # set gpu ids
        str_ids = opt.gpu_ids.split(',')
        opt.gpu_ids = []
        # for str_id in str_ids:
        #     id = int(str_id)
        #     if id >= 0:
        #         opt.gpu_ids.append(id)
        if len(opt.gpu_ids) > 0:
            pass
        #     torch.cuda.set_device(opt.gpu_ids[0])

        self.opt = opt
        return self.opt
