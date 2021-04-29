import os
import scanpy as sc
from os.path import join, exists
from os import listdir
import anndata
import scipy
import numpy as np
import sys
import gc

from utils import *

# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    return '{:.3} MB'.format(x.__sizeof__()/1e6)

def print_size_in_MB_sparse_matrix(a):
    # a = scipy.sparse.csr_matrix(np.random.randint(10, size=(40, 3)))
    # x = a.data.nbytes + a.indptr.nbytes + a.indices.nbytes
    size = a.data.size/(1024**2)
    return '{:.3} MB'.format(size)

import warnings
warnings.filterwarnings("ignore")

overwrite = False
for n_sample_per_batch in [500, 1000, None]:
    # examine types, columns and others incorporated in the object
    
    code_n_cells = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else ''))

    print(code_n_cells)

    print('# of cells (input argument)', n_sample_per_batch)
    
    code_output = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else '_all'))
    output_path = '../../data/integration_march_2021/input/input%s_cells.h5ad' % code_output
    print(output_path)            
    
    if exists(output_path) and not overwrite:
        continue

    dataset_names = ["Wong", "Scheetz", "Chen_c", "Hafler", "Roska", "Sanes", "Hackney", "Chen_b", 'Chen_a']

    # to avoid memory leaks do it in two rounds
    p1 = output_path.replace('.h5ad', '_part1.h5ad')

    if not exists(p1):
        print('loading', dataset_names[:4])
        ad1 = get_datasets(dataset_names[:4], code_n_cells=code_n_cells)

        print('ad1')
        print ('laoding datasets 1 done...')
        print(ad1.obs.dataset.value_counts())
        # save part1
         # save part1
        ad1 = ad1[ad1.obs.dataset.isin(set(dataset_names[:4])),:]
        ad1.write(p1, compression='lzf')
        del ad1
        print(p1)

    p2 = output_path.replace('.h5ad', '_part2.h5ad')
    if not exists(p2):
        print('loading', dataset_names[4:-1])
        ad2 = get_datasets(dataset_names[4:-1], code_n_cells=code_n_cells)
        print('ad2')
        print(ad2)
        print(ad2.obs.index)
        print ('laoding datasets 2 done...')
        print(ad2.obs.dataset.value_counts())

        # save part1
        ad2 = ad2[ad2.obs.dataset.isin(set(dataset_names[4:-1])),:]
        ad2.write(p2, compression='lzf')
        del ad2
        print(p2)   
        
    p3 = output_path.replace('.h5ad', '_part3.h5ad')
    if not exists(p3):
        print('loading', dataset_names[-1:])
        ad3 = get_datasets(dataset_names[-1:], code_n_cells=code_n_cells)
        print('ad2')
        print(ad3)
        print(ad3.obs.index)
        print ('laoding datasets 3 done...')
        print(ad3.obs.dataset.value_counts())

        ad3 = ad3[ad3.obs.dataset.isin(set(dataset_names[-1:])),:]
        ad3.write(p3, compression='lzf')
        del ad3
        print(p3)    

    gc.collect()
    
    ad1 = sc.read_h5ad(p1)
    ad2 = sc.read_h5ad(p2)
    ad3 = sc.read_h5ad(p3)

    # print(ad1.obs.dataset.value_counts())
    # print(ad2.obs.dataset.value_counts())

    gc.collect()
    print('concatenating...')
    ad_final = anndata.concat([ad1, ad2, ad3])
    
    
    gc.collect()
    print('done...')

    print('ad final')
    print(ad1.shape, ad2.shape)
    print(ad_final.shape)
    # print(ad_final.obs.index)

    # define a unified code for all categories
    ad_final.obs['batch.merged'] = ad_final.obs['dataset'].astype(str) + ':' + ad_final.obs['batch'].astype(str)
    ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').cat.codes
    # input_scib.obs['batch.merged'].value_counts()
    ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').astype(str)
    # print(ad_final.obs['batch.merged'].value_counts())

    # we only care about genes detected in at least X cells or more (X=50)
    # min_cells = 50
    # sc.pp.filter_genes(ad, min_cells=min_cells)


    ad_final = ad_final[ad_final.obs['batch.merged'].map(ad_final.obs['batch.merged'].value_counts().to_dict()) > 100,:]
    ad_final.obs['batch.merged'].value_counts()

    print('saving to output...')
    ad_final.write(output_path, compression='lzf')
    
    if exists(p1):
        os.remove(p1)
    if exists(p2):
        os.remove(p2)

    print('done...')
