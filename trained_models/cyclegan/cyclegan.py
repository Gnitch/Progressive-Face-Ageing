import time
from trained_models.cyclegan.options.train_options import TrainOptions
from models import create_model
import torch
from PIL import Image
from torchvision.utils import save_image
import torchvision.transforms as transforms
import os
# import models
# import trained_models.cyclegan.models as models

def denorm(img):
    stats = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
    return img * stats[1][0] + stats[0][0]

def ageProgressCyclegan(img_path, adhar):
    # opt = TrainOptions().parse()
    opt = TrainOptions()

    model = create_model(opt)
    model.setup(opt)    

    transform_list = []
    transform_list += [ transforms.Resize(size=[286,286], interpolation=Image.BICUBIC),
                        transforms.RandomCrop(size=(256,256), padding=None),   
                        transforms.RandomHorizontalFlip(p=0.5),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5, 0.5, 0.5),
                                            (0.5, 0.5, 0.5))]

    image = Image.open(img_path[1:])
    img_transform = transforms.Compose(transform_list)
    image = img_transform(image)
    image.unsqueeze_(0)

    # os.chdir("trained_models/cyclegan")
    trained_model = torch.load("trained_models/cyclegan/model.pth")
    trained_model.eval()
    img = trained_model(image)
    img = denorm(img)
    save_image(img, f'media/AgeProgress/cyclegan/{adhar}.png')



