import torch
import PIL
from torch.autograd import Variable
from torchvision.transforms import transforms
import time
import alexclass


class Alexjudge(object):
    def __init__(self):
        t1 = time.time()
        self.net = alexclass.alex()
        self.net.load_state_dict(torch.load("./model/alex1"))
        self.net.eval()
        self.transform = transforms.Compose([
            transforms.Resize(280, PIL.Image.BICUBIC),  # 缩放图片(Image)，保持长宽比不变，最短边为224像素
            transforms.CenterCrop(224),
            transforms.ToTensor(),  # 将图片(Image)转成Tensor，归一化至[0, 1]
            transforms.Normalize(mean=[.5, .5, .5], std=[.5, .5, .5])  # 标准化至[-1, 1]，规定均值和标准差
        ])
        # torch.save(self.net.state_dict(),"./model/alex1")
        print("初始化完成 耗时" + str((time.time() - t1)))

    def judge(self, filename=""):
        img = PIL.Image.open(filename)
        img1 = self.transform(img)
        img1 = torch.unsqueeze(img1, 0)
        img1 = Variable(img1, volatile=True)
        # print(img1)
        outputs = self.net(img1)
        _, ans = torch.max(outputs.data, 1)
        return str(int(ans[0]) + 1)
