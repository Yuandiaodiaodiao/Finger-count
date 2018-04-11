from torch.autograd import Variable
import torch
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

import  readfile
import matplotlib.pyplot as plt
import PIL
from torchvision.transforms import ToPILImage, transforms

show = ToPILImage()
transform4 = transforms.Compose([
        transforms.Resize(280,PIL.Image.BICUBIC), # 缩放图片(Image)，保持长宽比不变，最短边为224像素
        transforms.CenterCrop(224),
        transforms.ToTensor(), # 将图片(Image)转成Tensor，归一化至[0, 1]
        transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5]) # 标准化至[-1, 1]，规定均值和标准差
        ])
testsetsmall = ImageFolder('./数据集/train2', transform=transform4)
testsetsmallloader = DataLoader(testsetsmall, batch_size=1, shuffle=False, num_workers=1, drop_last=False)


def test2(net):

    net.eval()

    correct = 0
    total = 0
    for data in testsetsmallloader:
        images, labels = data
        # for i in readf.testsetsmall:
        #     (data, label) =i
        #     # print(classes[label])
        #
        #     # (data + 1) / 2是为了还原被归一化的数据
        #     img=show((data + 1) / 2).resize((224, 224))
        #     plt.imshow(img)
        #     plt.show()



        outputs = net(Variable(images))
        print(Variable(images))
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        print("data=",labels[0],"test=",predicted[0])
        correct += (predicted == labels).sum()
        # img = show((images[0] + 1) / 2).resize((224, 224))
        # plt.imshow(img)
        # plt.show()
    print('Accuracy on the small test : %d %%' % (100 * correct / total))

