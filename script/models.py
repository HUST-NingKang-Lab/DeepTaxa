#!/usr/bin/env python3
import torch as pt
import numpy as np
import pickle

from torch import nn,optim
from torch.autograd import Variable
from torch.nn.functional import dropout
from torch.nn.parameter import Parameter
from torch.utils.data import TensorDataset, DataLoader

class FELayer(nn.Module):
  def __init__(self, cin, cout):
    super(FELayer, self).__init__()
    chid = cout * 4
    print('#FELayer:\t%d\t%d\t%d' % (cin, chid, cout))

    self.fe = nn.Sequential(
        nn.Flatten(), nn.Linear(cin, chid),
        nn.GroupNorm(chid//16, chid), nn.GELU(), nn.Linear(chid, cout))

  def forward(self, x):
    return self.fe(x)

class ResLayer(nn.Module):
  def __init__(self, cio, dropout=0.5):
    super(ResLayer, self).__init__()
    chid = cio // 4
    print('#ResidualLayer:', cio, chid, cio)

    self.res = nn.Sequential(
        nn.GroupNorm(cio//16, cio), nn.GELU(), nn.Linear(cio, chid),
        nn.GroupNorm(cio//16, chid), nn.GELU(), nn.Linear(chid, chid),
        nn.GroupNorm(cio//16, chid), nn.GELU(), nn.Linear(chid, chid),
        nn.GroupNorm(cio//16, chid), nn.GELU(), nn.Linear(chid, cio),
        nn.Dropout(dropout))

  def forward(self, x):
    return x + self.res(x)

class ResBlock(nn.Module):
  def __init__(self, cio, depth, dropout=0.5):
    super(ResBlock, self).__init__()
    layers = [ResLayer(cio, dropout=dropout) for i in range(depth)]
    self.block = nn.Sequential(*layers)

  def forward(self, x):
    return self.block(x)

class CompLayer(nn.Module):
  def __init__(self, cin, cout):
    super(CompLayer, self).__init__()
    print('#CompLayer:', cin, cout)

    self.comp = nn.Sequential(
        nn.BatchNorm1d(cin), nn.GELU(), nn.Linear(cin, cout))
  def forward(self, x):
    return self.comp(x)

class OntLayer(nn.Linear):
  def __init__(self, cio, ontology, dropout=0.5):
    super(OntLayer, self).__init__(cio,cio)
    self.pre = nn.Sequential(nn.LayerNorm(cio), nn.GELU())
    self.mask = ontology
    self.post = nn.Dropout(dropout)
    print('#OntLayer:', cio, cio)

  def forward(self, x):
    xx = self.post(nn.functional.linear(self.pre(x), self.weight * self.mask, self.bias))
    return x+xx

class OntBlock(nn.Module):
  def __init__(self, cio, ontology, depth, dropout=0.5):
    super(OntBlock, self).__init__()
    layers = [OntLayer(cio, ontology, dropout=dropout) for i in range(depth)]
    self.block = nn.Sequential(*layers)

  def forward(self, x):
    return self.block(x)

class ONN4TC(nn.Module):
  def __init__(self, size_marker, size_genus, size_out, ontology, dropout=0.5):
    super(ONN4TC, self).__init__()
    width1, width2, depth1, depth2, depth3 = 128, 128, 4, 4, 1

    #self.embed1 = nn.Sequential(
    #    FELayer(size_marker, width1),
    #    ResBlock(width1, depth1, dropout=dropout))

    self.embed2 = nn.Sequential(
        FELayer(size_genus, width2),
        ResBlock(width2, depth2, dropout=dropout))

    self.head = nn.Sequential(
        #CompLayer(width1 + width2, size_out),
        CompLayer(width2, size_out),
        OntBlock(size_out, ontology, depth3, dropout=dropout))

  def forward(self, x1, x2):
    #xx1 = self.embed1(x1)
    xx2 = self.embed2(x2)
    #xx = pt.concat((xx1,xx2), dim=1)
    #xx = self.head(xx)
    xx = self.head(xx2)
    return xx


