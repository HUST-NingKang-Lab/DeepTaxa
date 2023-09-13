# DeepTaxa
![](https://img.shields.io/badge/status-alpha-brightgreen?style=flat-square&logo=appveyor) [![downloads](https://static.pepy.tech/badge/deeptaxa)](https://pepy.tech/project/deeptaxa) ![](https://img.shields.io/github/license/HUST-NingKang-Lab/DeepTaxa?style=flat-square&logo=appveyor)

[DeepTaxa](https://github.com/HUST-NingKang-Lab/DeepTaxa) is a powerful deep learning tool designed for taxonomic classification of bacterial genomes, shows an order of magnitude increase in accuracy while maintaining remarkable computational efficiency. Our evaluation results demonstrated that DeepTaxa is highly accurate at different resolutions, could achieve a taxonomic classification accuracy of >99% at the rank of phylum to genus. It can classify 1,000 genomes within an hour wall clock time when using 32 cores of CPU. DeepTaxa also infer taxonomic hints for novel genomes, even when neither family or genus information is available in the model.  Therefore, we anticipate that DeepTaxa will serve as a useful instrument to understand present and future microbial diversity in a wide range of microbiological and ecological settings. Moreover, DeepTaxa could serve as a complement for contemporary methods, with the aim of accelerating taxonomic knowledge discovery from the rich microbiome resources.
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
We recommend deploying ONN4ARG using `conda`.
```shell
# install via source codes
wget https://github.com/HUST-NingKang-Lab/DeepTaxa/releases/download/v0.3-alpha/DeepTaxa.zip
unzip DeepTaxa.zip
cd DeepTaxa
# create the environment
conda env create -f config/deeptaxa.yml
# activate the environment
conda activate deeptaxa
# add an executable permission for scripts
chmod +x script/*
# check installation
script/check.sh
# If all goes well, you'll see a result file called "pred.tsv" in the "data/" directory in a few minutes

# install via pip
pip install deeptaxa
#If installed via pip, please confirm the "config" and "script" directories are under the "DeepTaxa" directory.
```

## Usage
Before using DeepTaxa, make sure you have activated the deeptaxa environment by using `conda activate deeptaxa`.
```shell
# identify 120 bacterial markers genes with hmmer
script/hmmer.sh [-h|--help] [-i|--input] [-o|--output]
# alignment of marker genes with mmseqs2
script/mmseqs.sh [-h|--help] [-i|--input] [-s|--hsummary] [-t|--tmp] [-o|--output]
# convert alignment results into an array format hdf5 file
script/data.py [-h] [-i MMSEQS_RESULT_PATH] [-c CONFIG_FILE_PATH] [-f FILE] [-o OUTPUT]
# taxonomic classification of genomes
script/predict.py [-h] [-i INPUT] [-m MODEL] [-t TREE] [-O ONTOLOGY] [-f FILE] [-o OUTPUT]
```
The workflow will take  `genomes/genomes_name_protein.faa` as input, and finally store the predicted annotations in `data/pred.tsv` or any other path you specify in the `-o` argument of `predict.py`.
## Developers

   Name   |      Email      |      Affiliation
----------|-----------------|----------------------------------------------------------------------------------------
Yuguo Zha |hugozha@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
Haobo Zhang |M202272359@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
Kang Ning |ningkang@hust.edu.cn| School of Life Science and Technology, Huazhong University of Science & Technology
