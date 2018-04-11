from torch import optim
from torch.autograd import Variable
from torch.optim.lr_scheduler import MultiStepLR

import readfile
import torch.nn as nn
import torch
import  test
import logger

class train():

    def trains(self,net):
        self.logs=logger.logger()
        # logs.refline(1,"2334",1)
        # logs.refline(4,"2334",5)
        # logs.refline(1,"2334",6)
        # logs.refline()
        readf=readfile.readfile()
        aimat=float(0.0)
        # test.tests(net, 0, float(aimat), readf, self.logs)
        net.train(mode=True)
        torch.set_num_threads(8)
        criterion = nn.CrossEntropyLoss()  # use a Classification Cross-Entropy loss


        optimizer = optim.SGD([
            {'params': net.features.parameters(), 'lr': 0.00001},
            {'params': net.lin.parameters(), 'lr': 0.001},
        {'params': net.classifier.parameters(), 'lr': 0.0005}], momentum=0.9)
        # scheduler = MultiStepLR(optimizer, milestones=[10, 80], gamma=0.1)
        tot=0
        for epoch in range(2000):  # loop over the dataset multiple times
            # scheduler.step()
            running_loss = 0.0
            net.train(mode=True)
            for i, data in enumerate(readf.dataloader, 0):
                tot+=1
                # get the inputs
                inputs, labels = data

                # wrap them in Variable
                inputs, labels = Variable(inputs), Variable(labels)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward + backward + optimize
                outputs = net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()

                # print statistics
                running_loss += loss.data[0]

                if i % 25 == 24:  # print every 2000 mini-batches
                    print('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 25))

                    self.logs.defx=tot
                    # print(self.logs.defx)
                    self.logs.refline(running_loss / 25*100, "loss")
                    running_loss = 0.0
                    aimat=float(aimat)
                    aimat=test.tests(net,epoch,float(aimat),readf,self.logs)
                    net.train(mode=True)

            torch.save(net, "./mod2/handalexnet34")
            print("saved")


        print('Finished Training')