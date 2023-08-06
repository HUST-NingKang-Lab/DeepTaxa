#!/usr/bin/env python3
import sys
import os
import pickle
import h5py
import argparse
import numpy as np

from tqdm import tqdm, trange
from utils import *

parser = argparse.ArgumentParser(description='#please use this script to convert MMseqs results into an array format hdf5 file')
parser.add_argument('-i', '--mmseqs_result_path', default='./mmseqs_result', type=str, help='indicate the absolute directory path of mmseqs result, default is \'./mmseqs_result\'')
parser.add_argument('-c', '--config_file_path', default='./config', type=str, help='indicate the absolute directory path of config file, default is \'./config\'')
parser.add_argument('-f', '--file', default='./data/file.sav', type=str, help='indicate a new file to store the genome ID, default is \'./data/file.sav\'')
parser.add_argument('-o','--output', default='./data/data.h5', type=str, help='indicate a new file to store the hdf5 array data, default is \'./data/data.h5\'')
args = parser.parse_args()

#set arguement
mmseqs_result = args.mmseqs_result_path
config_file = args.config_file_path
files_fn = args.file
data_fn = args.output


#loading metadata
metafile = '%s/bac120_taxonomy_r214.tsv' % config_file

#generating the genome dictionary 
genomefile,genomelist = '%s/rep-genome-genus1083.lst' % config_file, []
with open(genomefile, 'r') as f:
  for line in f.readlines():
    genomelist.append(line.strip())
dicg = dict(zip(genomelist, range(len(genomelist))))

#generating the marker dictionary
markerfile,markerlst = '%s/marker_gene.list' % config_file, []
with open(markerfile, 'r') as f:
  for line in f.readlines():
    markerlst.append(line.strip())
dicm = dict(zip(markerlst, range(len(markerlst))))

#set data path
datapath_seq = mmseqs_result
files = os.listdir(datapath_seq)

with open(files_fn, 'wb') as f:
  pickle.dump(files, f)

#processing mmseqs features
md2 = np.zeros((1,120,1083), dtype=float)
gid = []
kk = 0
for ifn in tqdm(files, desc='#Processing MMseqs2 features:'):
  gid.append(ifn)
  kk += 1
  marker = os.listdir('%s/%s' % (datapath_seq, ifn))
  lftmp = np.zeros((120,1083), dtype=float)

  for lfn in marker:
    cnt = len(open(r"%s/%s/%s" % (datapath_seq, ifn, lfn),'r').readlines())
    if(cnt > 1):
      markid = dicm[lfn.split('_')[0]]
      ldl =  local_dataloader('%s/%s/%s' % (datapath_seq, ifn, lfn))
      tmpdic = dict(zip(ldl.target, range(len(ldl.target))))
      for idxg, keyy in enumerate(dicg.keys()):
        try:
          idyy = tmpdic[keyy]
          lftmp[markid, idxg] = ldl.scores[idyy,0]
        except KeyError:
          pass

  lftmp = lftmp.reshape(1, 120, 1083)
  md2 = np.concatenate((md2, lftmp), axis=0)

md2 = md2[1:]
print('data dimension:', md2.shape)

with h5py.File(data_fn,'w') as f:
  f.create_dataset('data2', data=md2)
print('done!')
