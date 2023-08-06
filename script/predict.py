#!/usr/bin/env python3
import torch as pt
import numpy as np
import pickle
import h5py
import sys
import warnings
import argparse

from torch import nn,optim
from torch.autograd import Variable
from torch.nn.functional import dropout
from torch.nn.parameter import Parameter
from torch.utils.data import TensorDataset, DataLoader

from DeepTaxa import utils
from DeepTaxa import models
from DeepTaxa.models import *

warnings.filterwarnings("ignore")
device = 'cuda' if pt.cuda.is_available() else 'cpu'

parser = argparse.ArgumentParser(description='#please use this script for taxonomic classification of genomes')
parser.add_argument('-i', '--input', default='./data/data.h5', type=str,   help='indicate the input hdf5 array data, default is \'./data/data.h5\'')
parser.add_argument('-m', '--model', default='./config/model.pth', type=str, help='indicate the model file, default is \'./config/model.pth\'')
parser.add_argument('-t', '--tree', default='./config/tree.out', type=str, help='indicate the ontology tree name file, default is \'./config/tree.out\'')
parser.add_argument('-O', '--ontology', default='./config/ontology.pkl', type=str, help='indicate the ontology tree structure file, default is \'./config/ontology.pkl\'')
parser.add_argument('-f',  '--file', default='./data/file.sav', type=str, help='indicate the genome ID file, default is \'./data/file.sav\'')
parser.add_argument('-o','--output', default='./data/pred.tsv', type=str,  help='indicate the output file, default is \'./data/pred.tsv\'')
args = parser.parse_args()

def h5reader(fn):
  with h5py.File(fn,'r') as fr:
    data2 = fr['data2'][:]
  return(data2)

treefn = args.tree
tree = utils.gen_tn(treefn)

test_ifn, model_fn, files_fn, ofn = args.input, args.model, args.file, args.output
test_data2 = h5reader(test_ifn)
test_data2 = pt.tensor(test_data2).float()
test_data2 = pt.reshape(test_data2, (test_data2.size(0), -1))

with open(args.ontology, 'rb') as f:
  otlg = pickle.load(f)
ontology = Variable(pt.from_numpy(otlg).float()).to(device)
model = ONN4TC(size_marker=120*2, size_genus=120*1083, size_out=1745, ontology=ontology).to(device)
model.load_state_dict(pt.load(model_fn, map_location=device))
model.eval()

with open(files_fn, 'rb') as f:
  files = pickle.load(f)

fw = open(ofn, 'w')
fw.write('#Genome_ID\tDomian\tPhylum\tClass\tOrder\tFamily\tGenus\n')

if(ofn):
  x1, x2 = pt.zeros(1,120,2), test_data2
  x1, x2 = x1.to(device), x2.to(device)
  y1 = model(x1, x2).cpu().detach().numpy()
  s0,s1,s2,s3,s4,s5,s6 = 0,1,42,113,288,662,1745
  y10,y11,y12,y13,y14,y15 = y1[:,s0:s1],y1[:,s1:s2],y1[:,s2:s3],y1[:,s3:s4],y1[:,s4:s5],y1[:,s5:s6]

  for i in range(y1.shape[0]):
    idx_d = np.argmax(y10[i])
    idx_p = np.argmax(y11[i]) + s1
    idx_c = np.argmax(y12[i]) + s2
    idx_o = np.argmax(y13[i]) + s3
    idx_f = np.argmax(y14[i]) + s4
    idx_g = np.argmax(y15[i]) + s5
    fw.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (files[i], tree[idx_d], tree[idx_p], tree[idx_c], tree[idx_o], tree[idx_f], tree[idx_g]))

fw.close()
print('#done!')
