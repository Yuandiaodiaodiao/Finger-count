from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import ToPILImage
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import PIL
import random
import time
import numpy
show = ToPILImage()

random.seed(time.time())
numpy.random.seed(int(time.time()))
transform = transforms.Compose([
# transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.05,0.05,0.05,0.001),
    transforms.RandomHorizontalFlip(),
#     transforms.RandomVerticalFlip(),
    transforms.RandomRotation(25,resample=PIL.Image.BICUBIC,expand=False),
    transforms.RandomResizedCrop(224,(0.85,0.95),(0.9,1.1),PIL.Image.BICUBIC),

        transforms.ToTensor(), # 转为Tensor
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), # 归一化
                             ])


testsetbig = ImageFolder('./数据集/train',transform=transform)
testsetbigloader = DataLoader(testsetbig, batch_size=4, shuffle=False, num_workers=2, drop_last=True)
if __name__=="__main__":
    random.seed(time.time())
    numpy.random.seed(int(time.time()))

    for e in range(100):
        for i in testsetbig:
            (data, label) =i
            # print(classes[label])

            # (data + 1) / 2是为了还原被归一化的数据
            img=show((data + 1) / 2).resize((224, 224))
            plt.imshow(img)
            plt.show()