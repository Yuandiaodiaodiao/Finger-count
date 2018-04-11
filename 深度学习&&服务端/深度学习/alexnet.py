import torchvision
import torch.nn as nn
import readfile
import test
import train
import torch
import types
import alexclass2
import test2

def forward(self, x):
    x = self.features(x)
    x = x.view(x.size(0), 256*6*6)

    x = self.classifier(x)
    x=self.lin(x)
    return x
loads=0
if __name__=="__main__":
    # net=torchvision.models.alexnet(pretrained=True)
    if loads==0:
        net=alexclass2.alex()
        netd=net.state_dict()
        tx=torch.load("./models/alexnet-owt-4df8aa71.pth")
        tx={k:v for k,v in tx.items() if k in netd}
        netd.update(tx)
        net.load_state_dict(netd)



    # for param in net.parameters():
    #     param.requires_grad = False
    # for param in net.classifier.parameters():
    #     param.requires_grad = True
    # setattr(torchvision.models.AlexNet,"lin",nn.Linear(1000,4))
    # net.forward = types.MethodType(forward, net)

    # net.classifier= nn.Sequential(
    #             nn.Dropout(),
    #             nn.Linear(2304, 1024),
    #             nn.ReLU(inplace=True),
    #             nn.Dropout(),
    #             nn.Linear(1024, 1024),
    #             nn.ReLU(inplace=True),
    #             nn.Linear(1024, 10),
    #         )
    if loads==1:
      net=torch.load("./mod2/handalexnet20k")
    # test2.test2(net)
    tra=train.train()
    tra.trains(net)






