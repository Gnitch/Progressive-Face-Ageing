import time
from options.train_options import TrainOptions
from models import create_model
import torch
from PIL import Image
from torchvision.utils import save_image
import torchvision.transforms as transforms


if __name__ == '__main__':
    opt = TrainOptions().parse()

    model = create_model(opt)
    model.setup(opt)    

    transform_list = []
    transform_list += [ transforms.Resize(size=[286,286], interpolation=Image.BICUBIC),
                        transforms.RandomCrop(size=(256,256), padding=None),   
                        transforms.RandomHorizontalFlip(p=0.5),
                        transforms.ToTensor(),
                        transforms.Normalize((0.5, 0.5, 0.5),
                                            (0.5, 0.5, 0.5))]

    image = Image.open('input/test.JPG')
    img_transform = transforms.Compose(transform_list)
    image = img_transform(image)
    image.unsqueeze_(0)

    trained_model = torch.load("model.pth")
    trained_model.eval()

    def denorm(img):
        stats = (0.5, 0.5, 0.5), (0.5, 0.5, 0.5)
        return img * stats[1][0] + stats[0][0]

    save_image(denorm(image),'results/young.png')
    img = trained_model(image)
    img = denorm(img)
    save_image(img,'results/old.png')



