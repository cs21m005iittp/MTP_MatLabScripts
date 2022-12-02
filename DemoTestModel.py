# -*- coding: utf-8 -*-
"""playvariables.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/189g8aY6YNV2o6em6AaiT_Xj4oSGZFpUU
"""

from os.path import dirname, join as pjoin
import scipy.io as sio

data_dir = pjoin(dirname(sio.__file__), 'matlab', 'tests')
mat_fname = pjoin("/content/tests/", 'Variables.mat')

mat_contents = sio.loadmat(mat_fname)

sorted(mat_contents.keys())

print(mat_contents["data"])

print(len(mat_contents["data"]))
Y_ground = mat_contents["data"][0][1][0]
X = mat_contents["data"][0][0]
print(len(X))
print(Y_ground)
import torch
t = torch.Tensor(X)
print(t.shape)
z=(X,Y_ground);
training_data = [];
training_data.append(z)
# print(training_data[0])

#data preparation code
for i in range(len(mat_contents["data"])):
  Y_ground = mat_contents["data"][0][1][0]
  X = mat_contents["data"][0][0]
  z=(X,Y_ground)
  training_data.append(z)

print(len(training_data))

from torch.utils.data import DataLoader
batch_size = 1
train_loader = DataLoader(training_data,batch_size = batch_size)


#checking shape of loaded data
dataiter = iter(train_loader)
x, y = next(dataiter)

print(x.shape)
print(y.shape)
print(type(y))

!pip install torchmetrics

import torch
from torch import nn
from torchmetrics.classification import Accuracy,Precision,Recall,F1Score
from torch.nn import Module
from torch.nn import Conv3d
from torch.nn import Linear
from torch.nn import Conv2d
from torch.nn import MaxPool2d
from torch.nn import ReLU
from torch.nn import LogSoftmax
from torch import flatten

class NN(nn.Module):
  def __init__(self,flatten_size):
    super(NN, self).__init__()
    self.conv1=Conv3d(4,6,2)
    self.relu=ReLU()
    self.conv2=Conv3d(6,6,(1,2,2))
    self.fc1=Linear(flatten_size,24)
    self.soft=nn.Softmax()
    # self.flatten=nn.flatten()
    
  def forward(self, x):
    
    x=self.conv1(x)
    x=self.relu(x)
    x=self.conv2(x)
    x = torch.flatten(x)
    x=self.fc1(x)

    
    x=self.soft(x)
    return x

device = "cuda" if torch.cuda.is_available() else "cpu"



dataiter = iter(train_loader)
x, y = next(dataiter)
print(x.shape)
x=torch.tensor(x).float()
print(x.shape)
c1 = Conv3d(4,6,2)
x=c1(x)
print(x.shape)
relu=ReLU()
x=relu(x)
print(x.shape)
c2=Conv3d(6,6,(1,2,2))
x=c2(x)
print(x.shape)
flatten = nn.Flatten()
x=flatten(x)
print(x.shape)
var_size = x.shape[1]

fc1 = Linear(x.shape[1], 24)
x=fc1(x)
print(x.shape)

print(x.shape[1])

def loss_function(y_pred,y_ground):
  # print(" inside loss  = ",y_pred.shape)
  loss=-y_ground*torch.log(y_pred + 0.001)
  
  t=loss.sum()
  return t

#train model
import torch.optim as optim
import torch.nn.functional as F
model = NN(var_size).to(device)
optimizer = optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
model.train()
for epoch in range(2):  # loop over the dataset multiple times

    running_loss = 0.0
    for i, data in enumerate(train_loader):


      # get the inputs; data is a list of [inputs, labels]
      # print(i)
      X, y = data

      # zero the parameter gradients
      
      # forward + backward + optimize
      # print(X.shape)
      # print(y.shape)
      pred = model(X.float())
      
      y_ground=y
      # print(pred.shape)
      # print(y_ground.shape)
      loss = loss_function(pred, torch.tensor(y_ground))
      optimizer.zero_grad()
      
      # print(loss.grad_fn)
      loss.backward()
      optimizer.step()

      # print statistics
      running_loss += loss.item()
      # if i % 100 == 0:    # print every 2000 mini-batches
      print(f'[{epoch + 1}, {i + 1:5d}] loss: {running_loss / 2000:.3f}')
      running_loss = 0.0

print('Finished Training')

accuracy,precision,recall,f1Score = 0,0,0,0
dataloader = train_loader
size = len(dataloader.dataset)
num_batches=1
model.eval()
test_loss,correct=0,0

with torch.no_grad():
  for X,y in dataloader:
    X,y=X.to(device),y.to(device)
    pred = model(X.float())
    print(y.reshape(24))
    print(pred.shape)
    y_grd = y
    test_loss += loss_function(pred, y_grd).item()
    correct += (pred.argmax() == y).type(torch.float).sum().item()
test_loss/=num_batches
correct/=size
print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

print ('Returning metrics... (cs21m005: xx)')
accuracy_val = Accuracy()
print('Accuracy :', accuracy_val(pred,y))
precision_val = Precision(average = 'macro', num_classes = 10)
print('precision :', precision_val(pred,y))

recall_val = Recall(average = 'macro', num_classes = 10)
print('recall :', precision_val(pred,y))
f1score_val = F1Score(average = 'macro', num_classes = 10)
print('f1_score :', f1score_val(pred,y))