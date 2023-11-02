import os
import scanpy as sc
from os.path import join, exists
from os import listdir
import anndata
import scipy
import numpy as np
import sys
import gc
import pandas as pd

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


combinations = [[['Hackney', 'Roska']], # ['Hackney', 'Roska', 'Hafler', 'Wong', 'Scheetz', 'Chen_b', 'Chen_c', 'Sanes', 'Chen_a'],
                ['Chen_b', 'Chen_c', 'Chen_a']]
    
dataset_codes = ['all', 'Chen']
# add Chen_a plus all others
for k in combinations[0]:
    if 'Chen' in k:
        continue
    combinations.append(combinations[1] + k)
    dataset_codes.append('Chen+%s' % '+'.join(k))

for x, y in zip(dataset_codes, combinations):
    print(x, y)

overwrite = False
for n_sample_per_batch in [None]: # , 500, None]:
    # if n_sample_per_batch != None:
    #    continue
    # if n_sample_per_batch != None and n_sample_per_batch != 500:
    #     continue
    # examine types, columns and others incorporated in the object
    
    code_n_cells = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else ''))

    print(code_n_cells)

    print('# of cells (input argument)', n_sample_per_batch)
    
    code_output = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else '_all'))

    for dataset_names_subset, dataset_code in zip(combinations, dataset_codes):
        
        output_path = '../../data/integration_march_2021/input/input%s_cells_%s.h5ad' % (code_output, dataset_code)
        print(exists(output_path), output_path)
        
        if exists(output_path):
            continue
        
        print('next path to be created')
        print(exists(output_path), output_path)
        print('')
        
        print(dataset_code, dataset_names_subset)
        p1 = output_path.replace('.h5ad', '_part1.h5ad')

        names1 = dataset_names_subset[:5]
        names2 = dataset_names_subset[5:-1]
        names3 = dataset_names_subset[-1:]
        
        
        
        if dataset_code != 'all':
            names1, names2, names3 = names1, [], []
        print(names1)
        print(names2)
        print(names3)
                
        if not exists(p1) and len(names1) > 0:
            ad1 = get_datasets(names1, code_n_cells=code_n_cells)

            print('ad1')
            print ('laoding datasets 1 done...')
            print(ad1.obs.dataset.value_counts())
            # save part1
             # save part1
            ad1 = ad1[ad1.obs.dataset.isin(set(names1)),:]
            
            gc.collect()
            ad1.write(p1, compression='lzf')
            del ad1
            print(p1)

        p2 = output_path.replace('.h5ad', '_part2.h5ad')
        if not exists(p2) and len(names2) > 0:
            print('loading', names2)
            ad2 = get_datasets(names2, code_n_cells=code_n_cells)
            print('ad2')
            print(ad2)
            print(ad2.obs.index)
            print ('laoding datasets 2 done...')
            print(ad2.obs.dataset.value_counts())

            # save part1
            ad2 = ad2[ad2.obs.dataset.isin(set(names2)),:]
            gc.collect()
            ad2.write(p2, compression='lzf')
            del ad2
            print(p2)   

        p3 = output_path.replace('.h5ad', '_part3.h5ad')
        if not exists(p3) and len(names3) > 0:
            print('loading', names3)
            ad3 = get_datasets(names3, code_n_cells=code_n_cells)
            print('ad2')
            print(ad3)
            print(ad3.obs.index)
            print ('laoding datasets 3 done...')
            print(ad3.obs.dataset.value_counts())

            ad3 = ad3[ad3.obs.dataset.isin(set(names3)),:]
            gc.collect()
            ad3.write(p3, compression='lzf')
            
            del ad3
            print(p3)    

        gc.collect()

        ad1, ad2, ad3 = None, None, None
        # filter: only the datasets subset can be in the object
        ad1 = sc.read_h5ad(p1) #  cache=True)
        ad1 = ad1[ad1.obs['dataset'].isin(set(dataset_names_subset))]
        
        print('composition ad1')
        print(ad1.shape)
        print(ad1.obs.dataset.value_counts())

        if exists(p2) and exists(p3):
            ad2 = sc.read_h5ad(p2) #  cache=True)
            ad3 = sc.read_h5ad(p3) #  cache=True)
            ad2 = ad2[ad2.obs['dataset'].isin(set(dataset_names_subset))]
            ad3 = ad3[ad3.obs['dataset'].isin(set(dataset_names_subset))]

            print('composition ad2')
            print(ad2.shape)
            print(ad2.obs.dataset.value_counts())
            print('composition ad3')
            print(ad3.shape)
            print(ad3.obs.dataset.value_counts())
            # print(ad2.obs.dataset.value_counts())

        gc.collect()
        print('concatenating...')
        ad_final = anndata.concat([ad1, ad2, ad3]) if (ad2 is not None and ad3 is not None) else ad1


        # print(ad1.shape, ad2.shape, ad3.shape)        
        gc.collect()
        print('done...')

        print('ad final')
        # print(ad1.shape, ad2.shape)
        print(ad_final.shape)
        # print(ad_final.obs.index)

        # define a unified code for all categories
        ad_final.obs['batch.merged'] = ad_final.obs['dataset'].astype(str) + ':' + ad_final.obs['batch'].astype(str)
        ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').cat.codes
        # input_scib.obs['batch.merged'].value_counts()
        ad_final.obs['batch.merged'] = ad_final.obs['batch.merged'].astype('category').astype(str)
        # print(ad_final.obs['batch.merged'].value_counts())
        
        # include the donor information
        donor = pd.read_csv('data/donor_details.tsv', sep='\t')
        donor['k'] = donor['file'].str.replace('.', '').str.replace('h5ad', '')
        donor['dataset'] = donor['k'].str.split('/').str[1]
        donor['filename'] = donor['k'].str.split('/').str[2]
        donor_by_filename = donor[['donor', 'filename']].set_index('filename')['donor'].to_dict()
        ad_final.obs['donor'] = ad_final.obs['filename'].map(donor_by_filename)
        
        
        ad_final.obs['batch_donor_dataset'] = ad_final.obs['donor'].astype(str) + ':' + ad_final.obs['dataset'].astype(str) + ':' + ad_final.obs['batch'].astype(str)

        print('before batch filter (n=100)')
        print(ad_final.shape)
        ad_final = ad_final[ad_final.obs['batch_donor_dataset'].map(ad_final.obs['batch_donor_dataset'].value_counts().to_dict()) > 100,:]
        ad_final.obs['batch_donor_dataset'].value_counts()

        ad_final.obs['batch_donor_dataset'] = ad_final.obs['batch_donor_dataset'].astype('category')
        
        print('after batch filter (n=100)')
        print(ad_final.shape)
        print('saving to output...')
        
        print('Dataset composition...')
        print(ad_final.obs['dataset'].value_counts())

        ad_final.write(output_path, compression='lzf')

        if exists(p1):
            os.remove(p1)
        if exists(p2):
            os.remove(p2)
        if exists(p3):
            os.remove(p3)
        
        print('done...')
        
        del ad_final
        gc.collect()
