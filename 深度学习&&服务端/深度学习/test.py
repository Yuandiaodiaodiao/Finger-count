from torch.autograd import Variable
import torch
import  readfile
import matplotlib.pyplot as plt

from torchvision.transforms import ToPILImage
show = ToPILImage()

def tests(net,tims=-1,aimat=float(0.0),readf=readfile.readfile(),logs=None):
    aimat = float(aimat)
    net.eval()
    correct = 0
    total = 0
    tot=0
    for data in readf.testsetsmallloader:

        images, labels = data
        outputs = net(Variable(images, volatile=True))
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum()
        if total>100:
            break

    print('现实 : %d %%' % (100 * correct / total))
    logs.refline((100 * correct / total), "现实正确率")
    if float(100 * correct / total)> float(aimat):
        aimat=float(aimat)
        aimat=float(100 * correct / total)
        print("正确率"+str(float(aimat))+"刷新数据")
        torch.save(net ,"./mod2/handalexnetmax34"+str(tims))
    # net.state_dict(),
    correct = 0
    total = 0

    for data in readf.testselfloader:
        tot += 1
        images, labels = data
        outputs = net(Variable(images, volatile=True))
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum()
        if tot>100:
            break
    print('自身 : %d %%' % (100 * correct / total))
    logs.refline((100 * correct / total), "自身正确率")
    return float(aimat)

