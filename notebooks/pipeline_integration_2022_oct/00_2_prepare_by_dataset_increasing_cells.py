#!/usr/bin/env python
# coding: utf-8

# ### 1. Verify that all data reported by Jin is in

# In[1]:


# %load_ext autoreload
# %autoreload 2


# In[2]:


import warnings
warnings.filterwarnings("ignore")

import scIB
import os
import scanpy as sc
from os.path import join
from os import listdir
import anndata

import numpy as np

import scipy


# In[3]:


# datadir_orig = '/mnt/f/workspace/theislab/retina/data/RNA'
datadir_orig = '/home/theislab/l_ibarra/workspace/theislab/retina/data/RNA'
# datadir_orig = '/storage/groups/ml01/datasets/projects/20210318_retinal_data_integration_ignacio.ibarra_malte.luecken'

# datadir_scran = '/mnt/znas/icb_zstore01/groups/ml01/workspace/ignacio.ibarra/theislab/retinal_scRNAseq_integration/data/integration_march_2021/scran'
# datadir_scran = '/mnt/f/workspace/theislab/retina/data/integration_oct_2022/scran'
datadir_scran = '/home/theislab/l_ibarra/workspace/theislab/retina/data/integration_oct_2022/scran'


# In[4]:


# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    print('{:.3} MB'.format(x.__sizeof__()/1e6))

### Use the scran related directory to map all the files we need to put together.
# filenames = [f for f in os.listdir(datadir_orig)]
# filenames_md5 = [f.strip() for f in open(os.path.join(datadir_orig, 'md5sum.txt'))]

filenames_md5 = [f.strip() for f in os.listdir(datadir_orig) if f.endswith(".h5ad")]

files = set()


# In[5]:


filenames_by_dataset = {}
for f in filenames_md5:
    # dataset, filename = f.split(' ')[-1].split('/')[-2:]
    dataset = f.split('_')[0] if not "Chen" in f else f.split('_')[0] + '_' + f.split('_')[1]
    filename = f
    print(dataset, filename)
    if not dataset in filenames_by_dataset:
        filenames_by_dataset[dataset] = []
    filenames_by_dataset[dataset].append(filename)


# In[6]:


filenames_by_dataset.keys()


# In[7]:


# get all files from a single directory
def get_by_dataset(dataset_name, filenames=None, n_sample=None):
    adatas = []
    
    if (filenames is None):
        filenames = [f for f in listdir(join(datadir_scran, dataset_name))]
    print('# datasets', len(filenames))
    for fi, f in enumerate(filenames):
        if len(adatas) % 20 == 0:
            print('loaded so far', len(adatas))
        p = join(datadir_scran, dataset_name, f)
        print(fi, p)
        ad = sc.read_h5ad(p)
        
        if n_sample is not None:
            idx_sample = ad.obs.sample(n_sample if n_sample < ad.shape[0] else ad.shape[0]).index
            ad = ad[ad.obs.index.isin(idx_sample),:]
            # print(ad.shape)        
        
        ad.obs['dataset'] = dataset_name
        ad.obs['filename'] = f.replace('.h5ad', '')
        adatas.append(ad)

    print('attempting concatenation..')
    for ad in adatas:
        print(ad.shape)
    return adatas[0].concatenate(adatas[1:]) # join='outer')


# In[12]:


from os.path import exists
for n_sample in [500, None]:
    for dataset in filenames_by_dataset:
        print(dataset)
        if 'Chen' in dataset:
            continue
        subsampling_code = ('_' + str(n_sample) if n_sample is not None else '')

        next_filename = '%s%s.h5ad' % (dataset, subsampling_code)

        outdir = datadir_scran.replace('scran', 'input/bydataset%s' % subsampling_code)
        print(outdir)

        if not exists(outdir):
            os.mkdir(outdir)
            
        path_by_dataset = join(outdir, '%s' % (next_filename))

        
        if exists(path_by_dataset):
            continue
            
        print(exists(path_by_dataset), path_by_dataset)
            
        ad = get_by_dataset(dataset, filenames=filenames_by_dataset[dataset])
        
        if n_sample is not None:
            sel_idx = ad.obs.groupby('batch').apply(lambda x: x.sample(min(n_sample, len(x)))).index.get_level_values(None)
            ad = ad[ad.obs.index.isin(sel_idx),:]
            # print(ad.obs.batch.value_counts())
            print(ad.shape)
        
        print(ad.shape)
        ad.write(path_by_dataset, compression='lzf')
        print(dataset, 'done...')

