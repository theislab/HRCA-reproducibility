import os
import scanpy as sc
from os.path import join, exists
from os import listdir
import anndata
import scipy
import numpy as np
import sys

# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    return '{:.3} MB'.format(x.__sizeof__()/1e6)

def print_size_in_MB_sparse_matrix(a):
    # a = scipy.sparse.csr_matrix(np.random.randint(10, size=(40, 3)))
    # x = a.data.nbytes + a.indptr.nbytes + a.indices.nbytes
    size = a.data.size/(1024**2)
    return '{:.3} MB'.format(size)


# examine types, columns and others incorporated in the object
bydataset_directory = '../../data/integration_march_2021/input/bydataset'

n_sample = int(sys.argv[1]) if len(sys.argv) >= 2 else None # None # 150 # None # 5000 # None # 5000
nCount_RNA_thr = 500

print('# of cells (input argument', n_sample)

import random
random.seed(500)

adatas = []

output_path = '../../data/integration_march_2021/input/input_%s_cells.h5ad' % (str(n_sample) if n_sample is not None else 'all')

def get_datasets(names):
    for f in names: # listdir(bydataset_directory):
        # if 'Chen' in f:
        #     continue
        f = f + '.h5ad'
        print(f)
        p = join(bydataset_directory, f)
        ad = sc.read(p)
        # print(ad.shape)
        # print(ad.obs.columns)
        # print(type(ad.X), ad.X.dtype)
        # print(type(ad.layers['counts']), ad.layers['counts'].dtype)


        # print('counts')    
        # print(ad.layers['counts'])
        # print('X')
        # print(ad.X)
        # print('')

        # print('before conversion')
        # print('full', print_size_in_MB(ad))
        # print('obs', print_size_in_MB(ad.obs))
        # print('var', print_size_in_MB(ad.var))
        # print('X', print_size_in_MB_sparse_matrix(ad.X))
        # print('counts', print_size_in_MB_sparse_matrix(ad.layers['counts']))

        ad.obs['cell.type'] = 'unassigned' if not 'scpred_prediction' in ad.obs else ad.obs['scpred_prediction']

        ad.layers['counts'] = ad.layers['counts'].astype('float32')
        print(type(ad.layers['counts']), ad.layers['counts'].dtype)

        # we only care about genes detected in at least X cells or more (X=50)
        # min_cells = 25
        # sc.pp.filter_genes(ad, min_cells=min_cells)

        # print('after conversion')    

        # normalize
        # print('normalization')
        sc.pp.normalize_per_cell(ad, counts_per_cell_after=1e5)
        sc.pp.log1p(ad)

        if n_sample is not None:
            sel_idx = ad.obs.groupby('batch').apply(lambda x: x.sample(min(n_sample, len(x)))).index.get_level_values(None)
            ad = ad[ad.obs.index.isin(sel_idx),:]
            print(ad.obs.batch.value_counts())

        # define a unified code for all categories
        

        
        # print('full', print_size_in_MB(ad))
        # print('obs', print_size_in_MB(ad.obs))
        # print('var', print_size_in_MB(ad.var))
        # print('X', print_size_in_MB_sparse_matrix(ad.X))
        # print('counts', print_size_in_MB_sparse_matrix(ad.layers['counts']))

        ad = ad[ad.obs['nCount_RNA'] > nCount_RNA_thr,:]

        # we need to filter genes individually, because in the biggest dataset this does not work (memory)
        min_cells = 50
        sc.pp.filter_genes(ad, min_cells=min_cells)
        # print('')            
        
        # print('updating names....')
        ad.obs.index = ad.obs.index + ':' + ad.obs['dataset'].astype(str) + ':' + ad.obs['batch'].astype(str)
        
        # print('names after updating')
        # print(ad.obs.index)
        print(ad.obs.dataset.value_counts())
        
        # removal of datasets not supposed to be in objects, that for some reason loaded (investigate)
        ad = ad[ad.obs.dataset.isin(set(names)),:]
        
        if ad.raw is not None:
            del ad.raw
        
        adatas.append(ad)
        
    print('objects before concatenation')
    for ai, ad in enumerate(adatas):
        print(ai)
        print(ad)
        print(ad.obs.index)
        print(ad.obs.index.value_counts())

    print('concatenating...')
    ad = anndata.concat(adatas)
    
    if ad.raw is not None:
        del ad.raw
    
    print('names upon integration')
    print(ad.obs.index)
    return ad

dataset_names = ["Wong", "Scheetz", "Chen_c", "Hafler", "Roska", "Chen_a", "Sanes", "Hackney", "Chen_b"]

# to avoid memory leaks do it in two rounds
p1 = output_path.replace('.h5ad', '_part1.h5ad')

if not exists(p1):
    print('loading', dataset_names[:4])
    ad1 = get_datasets(dataset_names[:4])
    
    print('ad1')
    print(ad1)
    print(ad1.obs.index)
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
    print('loading', dataset_names[4:])
    ad2 = get_datasets(dataset_names[4:])
    print('ad2')
    print(ad2)
    print(ad2.obs.index)
    print ('laoding datasets 2 done...')
    print(ad2.obs.dataset.value_counts())
    
    # save part1
    ad2 = ad2[ad2.obs.dataset.isin(set(dataset_names[4:])),:]
    ad2.write(p2, compression='lzf')
    del ad2
    print(p2)

ad1 = sc.read_h5ad(p1)
ad2 = sc.read_h5ad(p2)
print(ad1.obs.dataset.value_counts())
print(ad2.obs.dataset.value_counts())
ad_final = anndata.concat([ad1, ad2])


print('ad final')
print(ad_final)
print(ad_final.obs.index)
    
# define a unified code for all categories
ad_final.obs['batch.merged'] = ad_final.obs['dataset'].astype(str) + ':' + ad_final.obs['batch'].astype(str)
ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').cat.codes
# input_scib.obs['batch.merged'].value_counts()
ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').astype(str)
print(ad_final.obs['batch.merged'].value_counts())

# we only care about genes detected in at least X cells or more (X=50)
# min_cells = 50
# sc.pp.filter_genes(ad, min_cells=min_cells)
print('saving to output...')
ad_final.write(output_path, compression='lzf')
print('done...')