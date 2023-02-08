#!/usr/bin/env python
# coding: utf-8

# ### To execute the contents of this notebook as a python script, please execute
# `./run_ipynb_w_python.sh 00_3_prepare_scib_input`
# 
# ### This routine needs up to 200GB of RAM to concatenate the largest objects. For that reason, it is recommended to execute as a cluster command with higher memory.
# `sbatch submit_00_3_prepare_scib_input.sh`

# In[26]:


# %load_ext autoreload
# %autoreload 2


# In[27]:


log_dataset_k = 'integration_oct_2022'


# In[28]:


import os
import scanpy as sc
from os.path import join, exists
from os import listdir
import anndata
import scipy
import numpy as np
import sys
import pandas as pd

import utils

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


# In[29]:


combinations = [['Chen_a', 'Chen_rgc', 'Chen_b', 'Chen_c', 'Chang', 'Hackney', 'Roska', 'Hafler', 'Wong', 'Scheetz', 'Sanes'],
                ['Chen_b', 'Chen_c', 'Chen_a']]
    
dataset_codes = ['all', 'Chen']
# add Chen_a plus all others
for k in combinations[0]:
    if 'Chen' in k:
        continue
    combinations.append(combinations[1] + [k])
    dataset_codes.append('Chen+%s' % k)

combinations = combinations[:1]
dataset_codes = dataset_codes[:1]

for x, y in zip(dataset_codes, combinations):
    print(x, y)


# In[30]:


# combinations = [[['Hackney', 'Roska']], # ['Hackney', 'Roska', 'Hafler', 'Wong', 'Scheetz', 'Chen_b', 'Chen_c', 'Sanes', 'Chen_a'],
#                 ['Chen_a', 'Chen_b', 'Chen_c']]
    
# dataset_codes = ['all', 'Chen']
# # add Chen_a plus all others
# for k in combinations:
#     # if not 'Chen' in k:
#     #     continue
#     combinations.append(combinations[1] + k)
#     dataset_codes.append('Chen+%s' % '+'.join(k))

# # print(dataset_codes)

# combinations = combinations[-1:]
# dataset_codes = dataset_codes[-1:]


# In[31]:


dataset_codes


# In[32]:


import gc


# In[33]:


# add donor information
path_xlsx = '/lustre/groups/ml01/datasets/projects/20210318_retinal_data_integration_ignacio.ibarra_malte.luecken/20221611_redownload/chen_rna_atlas/processed_h5ad/atlasrna_metadata.xlsx'
xl = pd.ExcelFile(path_xlsx)
xl.sheet_names  # see all sheet names

donor = []
for sheet_name in xl.sheet_names:
    df2 = xl.parse(sheet_name)  # read a specific sheet to DataFrame
    # print(sheet_name, df.shape)
    df2['sheet_name'] = sheet_name
    donor.append(df2)
donor = pd.concat(donor).reset_index(drop=True)


# In[34]:


overwrite = False

tech_groups = {'sn': {'sn'}, 'sc': {'sc'}, 'sn+sc': {'sn', 'sc'}}
for n_sample_per_batch in [500, None,]: # [100, 500, 750, 1000, 1500, 2000]: # , 500, None]:
    for tech_group in tech_groups:
        # if n_sample_per_batch != None:
        #    continue
        # if n_sample_per_batch != None and n_sample_per_batch != 500:
        #     continue
        # examine types, columns and others incorporated in the object

        code_n_cells = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else ''))

        print(code_n_cells)

        print('# of cells (input argument)', n_sample_per_batch, '(None = all cells')

        code_output = (('_' + str(n_sample_per_batch) if n_sample_per_batch is not None else '_all'))

        for dataset_names_subset, dataset_code in zip(combinations, dataset_codes):

            output_path = '../../data/%s/input/input%s_cells_%s_%s.h5ad' % (log_dataset_k, code_output, dataset_code, tech_group)
            print(exists(output_path), output_path)

            # assert False
            if exists(output_path):
                continue

            # print(dataset_code, dataset_names_subset)
            p1 = output_path.replace('.h5ad', '_part1.h5ad')

            print(dataset_names_subset)
            names1 = dataset_names_subset[:1]
            names2 = dataset_names_subset[1:4]
            names3 = dataset_names_subset[3:]

            # if dataset_code != 'all':
            #     names1, names2, names3 = names1, [], []
            print('names1', names1)
            print('names2', names2)
            print('names3', names3)

            # assert False

            if not exists(p1) and len(names1) > 0:
                ad1 = utils.get_datasets(names1, code_n_cells=code_n_cells, dataset_code=log_dataset_k)

                print('ad1')
                print ('laoding datasets 1 done...')
                print(ad1.obs.dataset.value_counts())
                # save part1
                 # save part1
                ad1 = ad1[ad1.obs.dataset.isin(set(names1)),:]
                ad1.write(p1, compression='lzf')
                del ad1
                print(p1)

            p2 = output_path.replace('.h5ad', '_part2.h5ad')
            if not exists(p2) and len(names2) > 0:
                print('loading', names2)
                ad2 = utils.get_datasets(names2, code_n_cells=code_n_cells, dataset_code=log_dataset_k)
                print('ad2')
                print(ad2)
                print(ad2.obs.index)
                print ('laoding datasets 2 done...')
                print(ad2.obs.dataset.value_counts())

                # save part1
                ad2 = ad2[ad2.obs.dataset.isin(set(names2)),:]
                ad2.write(p2, compression='lzf')
                del ad2
                print(p2)   

            p3 = output_path.replace('.h5ad', '_part3.h5ad')
            if not exists(p3) and len(names3) > 0:
                print('loading', names3)
                ad3 = utils.get_datasets(names3, code_n_cells=code_n_cells, dataset_code=log_dataset_k)
                print('ad2')
                print(ad3)
                print(ad3.obs.index)
                print ('laoding datasets 3 done...')
                print(ad3.obs.dataset.value_counts())

                ad3 = ad3[ad3.obs.dataset.isin(set(names3)),:]
                ad3.write(p3, compression='lzf')
                del ad3
                print(p3)    

            gc.collect()

            ad1, ad2, ad3 = None, None, None
            # filter: only the datasets subset can be in the object
            ad1 = sc.read_h5ad(p1) #  cache=True)
            ad1 = ad1[ad1.obs['dataset'].isin(set(dataset_names_subset))]
            print(ad1.obs.dataset.value_counts())

            if exists(p2):
                ad2 = sc.read_h5ad(p2) #  cache=True)
                ad2 = ad2[ad2.obs['dataset'].isin(set(dataset_names_subset))]
                print(ad2.obs.dataset.value_counts())

            gc.collect()
            print('concatenating...')
            print(p1)
            print(p2)
            print(p3, 'pending ad1/ad2 concatenation')

            print('concatenating ad1/ad2')
            print(ad1.shape)
            print(ad2.shape)  
            
            ad1.layers['counts'] = ad1.layers['counts'].astype('int16')
            ad2.layers['counts'] = ad2.layers['counts'].astype('int16')
            gc.collect()
            ad_final = anndata.concat([ad1, ad2]) if (ad2 is not None) else ad1
            if ad1 is not None:
                del ad1
            if ad2 is not None:
                del ad2
            gc.collect()        

            if exists(p3):
                ad3 = sc.read_h5ad(p3) #  cache=True)
                ad3 = ad3[ad3.obs['dataset'].isin(set(dataset_names_subset))]
                print(ad3.obs.dataset.value_counts())
                # print(ad2.obs.dataset.value_counts())

            ad3.layers['counts'] = ad3.layers['counts'].astype('int16')
            gc.collect()
            
            print('concatenating ad_final/ad3')
            ad_final = anndata.concat([ad_final, ad3]) if (ad3 is not None) else ad_final

            # keep a log of the technogy
            ad_final.obs['tech'] = np.where(ad_final.obs['dataset'].astype(str).str.split('_').str[0].isin({'Chen', 'Hackney'}), 'sn', 'sc')
            if ad3 is not None:
                del ad3
                
            ad_final = ad_final[ad_final.obs['tech'].isin(tech_groups[tech_group])]
            print(ad_final.obs.groupby(['dataset', 'tech']).size())
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

            # include the donor information using the metadata path from 
            donor_by_filename = donor[['sampleid', 'donor']].set_index('sampleid')['donor'].to_dict()
            ad_final.obs['donor'] = ad_final.obs['filename'].map(donor_by_filename).astype(str)

            ad_final.obs['batch_donor_dataset'] = ad_final.obs['donor'].astype(str) + ':' + ad_final.obs['dataset'].astype(str) + ':' + ad_final.obs['batch'].astype(str)

            print('before batch filter (n=100)')
            print(ad_final.shape)
            ad_final = ad_final[ad_final.obs['batch_donor_dataset'].map(ad_final.obs['batch_donor_dataset'].value_counts().to_dict()) > 100,:]
            ad_final.obs['batch_donor_dataset'].value_counts()

            print(ad_final.obs.dataset.value_counts())

            ad_final.obs['batch_donor_dataset'] = ad_final.obs['batch_donor_dataset'].astype('category')

            print('after batch filter (n=100)')
            print(ad_final.shape)
            print('saving to output...')       

            # convert counts into int16
            ad_final.layers['counts'] = ad_final.layers['counts'].astype('int16')
            
            ad_final.write(output_path, compression='lzf')

            if exists(p1):
                os.remove(p1)
            if exists(p2):
                os.remove(p2)
            if exists(p3):
                os.remove(p3)

            print('done...')



# In[ ]:




