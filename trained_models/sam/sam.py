from argparse import Namespace
import os
import sys
import pprint
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as transforms

# print(os.listdir())
os.chdir("trained_models/sam/SAM")
# print(os.listdir())
sys.path.append(".")
sys.path.append("..")
# sys.path.append("utils/common")
from datasets.augmentations import AgeTransformer
from models.psp import pSp
from utils.common import tensor2im
os.chdir("../../../")


def ageProgressSam(img_path, adhar):


    EXPERIMENT_TYPE = 'ffhq_aging'

    EXPERIMENT_DATA_ARGS = {
        "ffhq_aging": {
            "model_path": "trained_models/sam/sam_model.pth",
            "image_path": img_path,
            "transform": transforms.Compose([
                transforms.Resize((256, 256)),
                transforms.ToTensor(),
                transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])
        }
    }

    EXPERIMENT_ARGS = EXPERIMENT_DATA_ARGS[EXPERIMENT_TYPE]


    model_path = EXPERIMENT_ARGS['model_path']
    # ckpt = torch.load(model_path, map_location='cpu')


    # opts = ckpt['opts']
    # pprint.pprint(opts)


    # opts['checkpoint_path'] = model_path


    net = torch.load(model_path)
    net.eval()
    # net.cuda()


    image_path = EXPERIMENT_DATA_ARGS[EXPERIMENT_TYPE]["image_path"]
    
    original_image = Image.open(img_path[1:]).convert("RGB")
    original_image = original_image.resize((256, 256))


    img_transforms = EXPERIMENT_ARGS['transform']
    input_image = img_transforms(original_image)


    target_ages = [30, 40, 50]
    age_transformers = [AgeTransformer(target_age=age) for age in target_ages]

    def run_on_batch(inputs, net):
        result_batch = net(inputs.float(), randomize_noise=False, resize=False)
        return result_batch


    # for each age transformed age, we'll concatenate the results to display them side-by-side
    results = np.array(original_image)
    for age_transformer in age_transformers:
        print(f"Running on target age: {age_transformer.target_age}")
        with torch.no_grad():
            input_image_age = [age_transformer(input_image.cpu()).to('cuda')]
            input_image_age = torch.stack(input_image_age)
            result_tensor = run_on_batch(input_image_age, net)[0]
            result_image = tensor2im(result_tensor)
            result_image = result_image.resize((256, 256))
            results = np.concatenate([results, result_image], axis=1)


    results = Image.fromarray(results)

    # save image at full resolution
    results.save(f"media/AgeProgress/sam/{adhar}.png")


