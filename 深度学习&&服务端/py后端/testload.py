import torch
import torchvision.models

net=torchvision.models.resnet18(pretrained=False)
# torch.save(net.state_dict(), "./model/alex2")
# net.load_state_dict(torch.load("./model/alex2"))
torch.save(net,"alex3.pth")
net=torch.load("alex3.pth")