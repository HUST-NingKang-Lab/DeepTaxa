#!/usr/bin/env python3
import sys
import numpy as np
import pandas as pd

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score

class dataloader(object):
  def __init__(self, fn):
    self.fn = fn

  def load_table(self):
    data = pd.read_csv(self.fn, sep='\t', header=0, index_col=0)
    arr = np.array(data.values)
    arr = arr.astype('float')
    #arr[arr[:,0] < 95] = 0
    arr = arr/100
    self.data = arr
    self.marker = list(data.index)

  def sorted_data(self, marker_list):
    idx = []
    for i,item in enumerate(marker_list):
      idx.append(self.marker.index(item))
    idx = np.array(idx, dtype=int)
    sorted_data = self.data[idx]
    prof_mask = sorted_data[:,0] < 0.95
    sorted_data[prof_mask] = 0
    return(sorted_data, prof_mask)

class metaloader(object):
  def __init__(self, fn):
    self.fn = fn

  def load_table(self):
    gid,taxonomy = [],[]
    with open(self.fn, 'r') as f:
      for line in f.readlines():
        gid.append(line.strip().split('\t')[0])
        taxonomy.append(line.strip().split('\t')[1])
    dictionary = dict(zip(gid,taxonomy))
    self.gid = gid
    self.taxonomy = taxonomy
    self.maps = dictionary

class labelgenerator(object):
  def __init__(self, metafn, snlst):
    self.metafn = metafn
    self.snlst = snlst

  def get_meta(self):
    ml = metaloader(self.metafn)
    ml.load_table()
    dic = ml.maps
    taxalst = []
    for item in self.snlst:
      taxalst.append(dic[item])
    return(taxalst)

  def get_label(self):
    taxalst = self.get_meta()
    tn,tc,ontology = makeontology(taxalst)
    label = np.zeros((len(taxalst),len(tn)), dtype=np.int32)
    for i,item in enumerate(taxalst):
      path = item.split(';')
      for j in range(len(path)):
        label[i, tn.index(path[j])] = 1
    return(label)

class gen_label(object):
  def __init__(self, tn, metafn, snlst):
    self.tn = tn
    self.metafn = metafn
    self.snlst = snlst

    ml = metaloader(self.metafn)
    ml.load_table()
    dic = ml.maps
    taxalst = []
    for item in self.snlst:
      taxalst.append(dic[item])
    self.taxalst = taxalst

  def get_label(self):
    label = np.zeros((len(self.snlst),1745), dtype=np.int)
    for i,item in enumerate(self.taxalst):
      item = item.split(';')
      for j in range(len(item)):
        try:
          idx1 = self.tn.index(item[j])
          label[i, idx1] = 1
        except Exception as r:
          pass
    return(label)

def gen_tn(treefn):
  tn = []
  with open(treefn, 'r') as f:
    for line in f.readlines():
      tn.append(line.strip().split('\t')[1])
  return(tn[:1745])

def makeontology(taxonomy):
  lst = [[],[],[],[],[],[],[]]
  for item in taxonomy:
    path = item.split(';')
    for i,taxon in enumerate(path):
      lst[i].append(taxon)

  #dereplication
  for i in range(len(lst)):
    tmp = lst[i]
    lst[i] = list(set(tmp))
    lst[i].sort(key = tmp.index)

  #compute taxa name&count
  taxa_name,taxa_count = [],[]
  for item in lst:
    taxa_name.extend(item)
    taxa_count.append(len(item))

  #encode ontology
  arr1 = np.zeros((len(taxa_name), len(taxa_name)), dtype=int)
  for i in range(arr1.shape[0]):
    arr1[i,i] = 1

  for item in taxonomy:
    item = item.split(';')
    if(len(item) > 1):
      for i in range(len(item)-1):
        a,b = item[i],item[i+1]
        idxa,idxb = taxa_name.index(a),taxa_name.index(b)
        arr1[idxa,idxb] = 1
        arr1[idxb,idxa] = 1
  return(taxa_name,taxa_count,arr1)

def computescore(y1,y2):
  acc = accuracy_score(y1, y2)
  pr = precision_score(y1, y2, average='weighted')
  rc = recall_score(y1, y2, average='weighted')
  f1 = f1_score(y1, y2, average='weighted')
  return(acc, pr, rc, f1)

def evaluate(y1,y2):
  s0,s1,s2,s3,s4,s5,s6 = 0,1,42,113,288,662,1745
  y10,y11,y12,y13,y14,y15 = y1[:,s0:s1],y1[:,s1:s2],y1[:,s2:s3],y1[:,s3:s4],y1[:,s4:s5],y1[:,s5:s6]
  #y10,y11,y12,y13,y14,y15 = y1[:,0:1],y1[:,1:42],y1[:,42:113],y1[:,113:288],y1[:,288:662],y1[:,662:1745]
  y10[:,np.argmax(y10, axis=1)] = 1
  y10[y10 != 1] = 0
  for i in range(y11.shape[0]):
    y11[i,np.argmax(y11, axis=1)[i]] = 1
  y11[y11 != 1] = 0
  for i in range(y12.shape[0]):
    y12[i,np.argmax(y12, axis=1)[i]] = 1
  y12[y12 != 1] = 0
  for i in range(y13.shape[0]):
    y13[i,np.argmax(y13, axis=1)[i]] = 1
  y13[y13 != 1] = 0
  for i in range(y14.shape[0]):
    y14[i,np.argmax(y14, axis=1)[i]] = 1
  y14[y14 != 1] = 0
  for i in range(y15.shape[0]):
    y15[i,np.argmax(y15, axis=1)[i]] = 1
  y15[y15 != 1] = 0
  #for i in range(y16.shape[0]):
  #  y16[i,np.argmax(y16, axis=1)[i]] = 1
  #y16[y16 != 1] = 0

  y1 = np.concatenate((y10,y11,y12,y13,y14,y15), axis=1)
  cnt0,cnt1,cnt2,cnt3,cnt4,cnt5 = 0,0,0,0,0,0

  for i in range(y1.shape[0]):
    if((y1[i,s0:s1] == y2[i,s0:s1]).all()):
      cnt0 += 1
    if((y1[i,s1:s2] == y2[i,s1:s2]).all()):
      cnt1 += 1
    if((y1[i,s2:s3] == y2[i,s2:s3]).all()):
      cnt2 += 1
    if((y1[i,s3:s4] == y2[i,s3:s4]).all()):
      cnt3 += 1
    if((y1[i,s4:s5] == y2[i,s4:s5]).all()):
      cnt4 += 1
    if((y1[i,s5:s6] == y2[i,s5:s6]).all()):
      cnt5 += 1

  emr0 = cnt0/y1.shape[0]
  emr1 = cnt1/y1.shape[0]
  emr2 = cnt2/y1.shape[0]
  emr3 = cnt3/y1.shape[0]
  emr4 = cnt4/y1.shape[0]
  emr5 = cnt5/y1.shape[0]

  ACC0,PR0,RC0,F10 = computescore(y2[:,s0:s1], y1[:,s0:s1])
  ACC1,PR1,RC1,F11 = computescore(y2[:,s1:s2], y1[:,s1:s2])
  ACC2,PR2,RC2,F12 = computescore(y2[:,s2:s3], y1[:,s2:s3])
  ACC3,PR3,RC3,F13 = computescore(y2[:,s3:s4], y1[:,s3:s4])
  ACC4,PR4,RC4,F14 = computescore(y2[:,s4:s5], y1[:,s4:s5])
  ACC5,PR5,RC5,F15 = computescore(y2[:,s5:s6], y1[:,s5:s6])

  print('#Rank\tEMR\tAc\tPr\tRc\tF1')
  print('#D\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr0,ACC0,PR0,RC0,F10))
  print('#P\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr1,ACC1,PR1,RC1,F11))
  print('#C\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr2,ACC2,PR2,RC2,F12))
  print('#O\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr3,ACC3,PR3,RC3,F13))
  print('#F\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr4,ACC4,PR4,RC4,F14))
  print('#G\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f' % (emr5,ACC5,PR5,RC5,F15))

  return(emr0,emr1,emr2,emr3,emr4,emr5)

class local_dataloader(object):
  def __init__(self, fn):
    self.fn = fn
    df = pd.read_csv(self.fn, sep='\t', header=0, index_col=0)
    self.target = df.values[:, 0]
    self.scores = np.array(df.values[:, 1:], dtype=float)

