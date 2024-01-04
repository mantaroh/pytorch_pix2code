#!/usr/bin/env python
# coding: utf-8

# In[1]:


from util import UIDataset, Vocabulary
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch
from torch.utils.data import DataLoader
from model import *
from torchvision import transforms
from PIL import Image


# In[2]:


dataset = UIDataset('./dataset/training', 'voc.pkl')


# # Training

# In[3]:


net = Pix2Code().cuda()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(net.parameters(), lr = 0.0001)


# In[5]:


for epoch in range(10):
    net.zero_grad()
    for j, data in enumerate(dataset):
        image, context, prediction = data
        image = image.unsqueeze(0).cuda()
        context = context.unsqueeze(0).cuda()
        prediction = prediction.cuda()
        output = net(image, context)
        output = output.squeeze(0)
        prediction = torch.argmax(prediction, 1)
        loss = criterion(output, prediction)
        loss.backward()
        if j%10 == 0:
            optimizer.step()
            print('Loss: {}, Epoch: {}'.format(loss.data, epoch))
            net.zero_grad()

torch.save(net.state_dict(), './pix2code.weights')


# # Testing

# In[6]:


net = Pix2Code()
net.load_state_dict(torch.load('./pix2code.weights'))
net.cuda().eval()


# In[7]:


test_data = UIDataset('./dataset/evaluation', 'voc.pkl')
vocab = Vocabulary('voc.pkl')


# In[17]:


image, *_ = test_data.__getitem__(np.random.randint(len(test_data)))
t = transforms.ToPILImage()
image = image.unsqueeze(0)
t(image.squeeze())


# In[23]:


image = image.cuda()
ct = []
ct.append(vocab.to_vec(' '))
ct.append(vocab.to_vec('<START>'))
output = ''
for i in range(200):
    context = torch.tensor(ct).unsqueeze(0).float().cuda()
    index = torch.argmax(net(image, context), 2).squeeze()[-1:].squeeze()
    v = vocab.to_vocab(int(index))
    if v == '<END>':
        break
    output += v
    ct.append(vocab.to_vec(v))

with open('./compiler/output.gui', 'w') as f:
    f.write(output)

print(output)


# Now from the compiler directory in your terminal run
# `python web-compiler.py output.gui`.
# This will generate a `output.html` file that you can open in your browser.
