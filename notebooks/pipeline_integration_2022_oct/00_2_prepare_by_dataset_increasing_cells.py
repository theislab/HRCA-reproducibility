#!/usr/bin/env python
# coding: utf-8

# ### 1. Verify that all data reported by Jin is in

# In[1]:


# %load_ext autoreload
# %autoreload 2


# In[2]:


import scanpy as sc
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


import glob
# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    print('{:.3} MB'.format(x.__sizeof__()/1e6))

### Use the scran related directory to map all the files we need to put together.
datasets_scran = '/lustre/groups/ml01/workspace/ignacio.ibarra/theislab/retina/data/integration_oct_2022/scran'
paths_h5ad = glob.glob(datasets_scran + '/*/*.h5ad')
print(len(paths_h5ad))
# filenames_md5 = [f.strip() for f in open(os.path.join(datadir_orig, 'md5sum.txt'))]


# In[4]:


filenames_by_dataset = {}
for path_h5ad in paths_h5ad:
    # print(f)
    dataset = path_h5ad.split('/')[-2]
    # print(dataset, os.path.basename(path_h5ad))
    if not dataset in filenames_by_dataset:
        filenames_by_dataset[dataset] = []
    filenames_by_dataset[dataset].append(path_h5ad)


# In[5]:


print(filenames_by_dataset.keys())
print(filenames_by_dataset['Chen_a'])


# In[6]:


# get all files from a single directory
def get_by_dataset(dataset_name, filenames=None, n_sample=None):
    adatas = []
    
    if (filenames is None):
        filenames = [f for f in listdir(join(datasets_scran, dataset_name))]
    print('# datasets', len(filenames))
    for f in filenames:
        if len(adatas) % 20 == 0:
            print('loaded so far', len(adatas))
        p = join(datasets_scran, f)
        # print(p)
        ad = sc.read_h5ad(p)
        
        if n_sample is not None:
            idx_sample = ad.obs.sample(n_sample if n_sample < ad.shape[0] else ad.shape[0]).index
            ad = ad[ad.obs.index.isin(idx_sample),:]
            # print(ad.shape)        
        
        ad.obs['dataset'] = dataset_name
        ad.obs['filename'] = f.replace('.h5ad', '')
        adatas.append(ad)
    return adatas[0].concatenate(adatas[1:]) # join='outer')


# In[ ]:


from os.path import exists
for n_sample in [100,]: #  200, 500, None]: # 500, 1000, None]:
    for dataset in filenames_by_dataset:
        print(dataset)

        subsampling_code = ('_' + str(n_sample) if n_sample is not None else '')
        next_filename = '%s%s.h5ad' % (dataset, subsampling_code)
        outdir = '../../data/integration_oct_2022/input/bydataset%s' % subsampling_code
        if not exists(outdir):
            os.makedirs(outdir)
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
        
        if ad.raw is not None:
            del ad.raw
        
        # convert counts into int16
        ad.layers['counts'] = ad.layers['counts'].astype('int16')        
        ad.write(path_by_dataset, compression='lzf')
        print(dataset, 'done...')        
    

