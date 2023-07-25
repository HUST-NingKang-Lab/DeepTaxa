# DeepTaxa
![](https://img.shields.io/badge/status-alpha-brightgreen?style=flat-square&logo=appveyor) [![downloads](https://static.pepy.tech/badge/onn4arg)](https://pepy.tech/project/onn4arg) [![](https://img.shields.io/badge/DOI-10.1101/2021.07.30.454403-brightgreen?style=flat-square&logo=appveyor)](https://www.biorxiv.org/content/10.1101/2021.07.30.454403) ![](https://img.shields.io/github/license/HUST-NingKang-Lab/DeepTaxa?style=flat-square&logo=appveyor)

[DeepTaxa](https://github.com/HUST-NingKang-Lab/DeepTaxa) is a deep learning tool for taxonomic classification of bacterial genomes, shows an order of magnitude increase in efficiency without loss of accuracy. DeepTaxa achieved a taxonomic classification accuracy of >99% at the rank of genus and provided reliable taxonomic clues at the rank of family or higher. More importantly, DeepTaxa is well optimized to run on a personal laptop with single core of CPU and less than 16 GB of RAM without the need of a graphic card. It can classify about 1000 genomes within 1 hour wall clock time when using 32 cores of CPU. DeepTaxa provides classification from the rank of phylum to genus; more resolved classification like species need to be supplemented by other tools, such as [FastANI](https://github.com/ParBLiSS/FastANI). We believe DeepTaxa will be a good complement for GTDB-Tk v2, with the aim of accelerating taxonomic knowledge discovery of microbial kingdom.
## Requirements
- Linux operating system
- At least 16 GB of RAM

## Dependency
- [Python 3.9.16](https://www.python.org/downloads/release/python-3916/)
- [Pytorch 1.13.1](https://github.com/pytorch/pytorch)
- [NumPy 1.25.1](https://numpy.org/)
- [pandas 2.0.3](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [h5py 3.8.0](https://pypi.org/project/h5py/)
- [tqdm 4.65.0](https://tqdm.github.io/)
- [scikit-learn 1.3.0](https://scikit-learn.org/stable/index.html)
- [hmmer 3.1b2](http://hmmer.org/)
- [mmseqs 14.7e284](https://github.com/soedinglab/MMseqs2)
- [r-base 4.2.0](https://anaconda.org/r/r-base)

## Installation
We recommend deploying ONN4ARG using `git` and `conda`.
```shell
# create the environment
conda env create -f deeptaxa.yml
# activate the environment
conda activate deeptaxa
# install via source codes
wget https://
tar zxf onn4arg-v1.0-model.tar.gz
# check installation
check.sh
# If all goes well, you'll see a result file called "pred.tsv" in the "data/" directory in a few minutes
```

## Usage
Before using DeepTaxa, make sure you have activated the deeptaxa environment by using `conda activate deeptaxa`.
```shell
# identify 120 bacterial markers genes with hmmer
script/hmmer.sh [-h|--help] [-i|--input] [-o|--output]
# alignment of marker genes with mmseqs2
script/mmseqs.sh [-h|--help] [-i|--input] [-s|--hsummary] [-t|--tmp] [-o|--output]
# convert alignment results into an array format hdf5 file
script/data.py [-h] [-p PATH] [-f FILE] [-o OUTPUT]
# taxonomic classification of genomes
script/predict.py [-h] [-i INPUT] [-m MODEL] [-f FILE] [-o OUTPUT]
```
The workflow will take  `genomes/genomes_name_protein.faa` as input, and finally store the predicted annotations in `data/pred.tsv` or any other path you specify in the `-o` argument of `predicti.py`.
## Developers

   Name   |      Email      |      Affiliation
----------|-----------------|----------------------------------------------------------------------------------------
Yuguo Zha |hugozha@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
Haobo Zhang |M202272359@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
Kang Ning |ningkang@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
