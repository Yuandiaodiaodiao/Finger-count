import torchvision
import torch
import torchvision.transforms as transforms
import PIL
# torchvision数据集的输出是在[0, 1]范围内的PILImage图片。
# 我们此处使用归一化的方法将其转化为Tensor，数据范围为[-1, 1]
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder


class readfile():
    def __init__(self):
        self.transform = transforms.Compose([
            transforms.Resize(224),
            # transforms.RandomCrop(224),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),
        ])
        self.trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=False, transform=self.transform)
        self.trainloader = torch.utils.data.DataLoader(self.trainset, batch_size=4,
                                                  shuffle=False, num_workers=2)

        self.testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=False, transform=self.transform)
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=4,
                                                 shuffle=True, num_workers=2)
        self.classes = ('plane', 'car', 'bird', 'cat',
                   'deer', 'dog', 'frog', 'horse', 'ship', 'truck')
        self.transform2 = transforms.Compose([
# transforms.RandomHorizontalFlip(),
    transforms.ColorJitter(0.05,0.05,0.05,0.001),
    transforms.RandomHorizontalFlip(),
#     transforms.RandomVerticalFlip(),
    transforms.RandomRotation(25,resample=PIL.Image.BICUBIC,expand=False),
    transforms.RandomResizedCrop(224,(0.80,1),(0.9,1.1),PIL.Image.BICUBIC),

        transforms.ToTensor(), # 转为Tensor
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)), # 归一化
                             ])
        self.transform3 = transforms.Compose([
        transforms.Resize(224,PIL.Image.BICUBIC), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
        transforms.CenterCrop(224),
        transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]
        transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5]) # 标准化至[-1, 1]，规定均值和标准差
        ])
        self.transform4 = transforms.Compose([
        transforms.Resize(280,PIL.Image.BICUBIC), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
        transforms.CenterCrop(224),
        transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]
        transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5]) # 标准化至[-1, 1]，规定均值和标准差
        ])
        self.dataset = ImageFolder('./数据集/train34',transform=self.transform2)
        self.dataloader = DataLoader(self.dataset, batch_size=4, shuffle=True, num_workers=2, drop_last=True)
        self.testsetbig = ImageFolder('./数据集/bigtest',transform=self.transform3)
        self.testsetbigloader = DataLoader(self.testsetbig, batch_size=4, shuffle=True, num_workers=2, drop_last=True)
        self.testsetsmall = ImageFolder('./数据集/train34test',transform=self.transform4)
        self.testsetsmallloader = DataLoader(self.testsetsmall, batch_size=1, shuffle=False, num_workers=1, drop_last=False)
        self.testself = ImageFolder('./数据集/train34', transform=self.transform3)
        self.testselfloader = DataLoader(self.testself, batch_size=1, shuffle=True, num_workers=2,drop_last=True)
