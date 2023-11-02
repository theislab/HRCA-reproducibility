#!/usr/bin/env python
# coding: utf-8

# In[2]:


# !which python


# In[3]:


# for some reason the import of scgen in cluster fails if anndata is not imported first.
import anndata
import scgen
scgen.__version__


# In[4]:



import scIB
import numpy as np
import scanpy as sc
# ls -ltrh /storage/groups/ml01/workspace/ignacio.ibarra/theislab/retinal_scRNAseq_integration/data/integration_march_2021/input/input*_cells.h5ad
import os
from os.path import exists, join
from os import makedirs
import pandas as pd
# ad = sc.read_h5ad('/home/icb/ignacio.ibarra/theislab/scIB_output/retinal_all_batch_donor_dataset_cell.type/prepare/unscaled/HVG.2K/adata_pre.h5ad')
# ad.shape
### here we write a version of the script in where we are sampling Chen_a/b/c


# In[ ]:





# In[5]:


import sys

print(sys.argv)
query = sys.argv[1] # 'heart_ventricle' # 'heart_ventricle', 'heart_atrial'

if query == '-f':
    query = 0
else:
    query = int(query)

# read queries from dataframe path
# df = pd.read_csv('queries_gpu_methods.csv', index_col=0)
df = pd.read_csv('queries_gpu_methods.csv', index_col=0)


# In[6]:


df.shape


# In[7]:


# !pip3 install torch==1.9.0+cu111 torchvision==0.10.0+cu111 torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html


# In[8]:


## What really works seems to be having the tf-nightly installation with latest keras, and modifying scgen to allow tf.keras.optimizers
# pip install tf-nightly


# In[9]:


import torch
print('pytorch + cuda')
print(torch.__version__)


# In[10]:


import keras
print(keras.__version__)


# In[11]:


# # import tensorflow as tf
# import tensorflow.compat.v1 as tf
# tf.disable_v2_behavior() 
# print(tf.__version__)


# In[12]:


print('scgen')
from tensorflow.python.client import device_lib
devices = device_lib.list_local_devices()
print('# of detected devices', len(devices))
for di, device in enumerate(devices):
    print(di, device.name)


# In[13]:


# print(df)
for p in  df['input']:
    if not exists(p):
        print(exists(p), p)
for p in  df['output']:
    if not exists(p):
        print(exists(p), p)


# In[14]:


## Function to make umap
def reduce_data(adata, batch_key=None, subset=False,
                filter=True, flavor='cell_ranger', n_top_genes=2000, n_bins=20,
                pca=True, pca_comps=50, overwrite_hvg=True,
                neighbors=True, use_rep='X_pca', 
                umap=True):
    """
    overwrite_hvg:
        if True, ignores any pre-existing 'highly_variable' column in adata.var
        and recomputes it if `n_top_genes` is specified else calls PCA on full features.
        if False, skips HVG computation even if `n_top_genes` is specified and uses
        pre-existing HVG column for PCA
    """
    
    print('setting up HVGs')
    assert n_top_genes == adata.shape[1]
    adata.var["highly_variable"] = True
    n_hvg = np.sum(adata.var["highly_variable"])
        
    print('PCA and/or neighbors')
    if pca:
        print("PCA")
        use_hvgs = not overwrite_hvg and "highly_variable" in adata.var
        sc.tl.pca(adata,
                  n_comps=pca_comps, 
                  use_highly_variable=use_hvgs, 
                  svd_solver='arpack', 
                  return_info=True)
    
    if neighbors:
        n_jobs = 4
        print("Nearest Neigbours")
        sc.settings.n_jobs = n_jobs
        from joblib import parallel_backend
        import time
        start_time = time.time()
        with parallel_backend('threading', n_jobs=n_jobs): sc.pp.neighbors(adata, use_rep=use_rep)
        print("--- %s seconds ---" % (time.time() - start_time))
    
    if umap:
        print("UMAP")
        start_time = time.time()
        sc.tl.umap(adata)
        print("--- %s seconds ---" % (time.time() - start_time))
        
    # print('before return')
    # print(adata)


# In[15]:


dataset_names = ['Chen_a', 'Chen_b', 'Chen_c', 'Hackney', 'Hafler', 'Roska', 'Wong', 'Scheetz', 'Sanes']
dataset_names


# In[16]:


import matplotlib.pyplot as plt


# In[17]:


df_bkp = df.copy()


# In[18]:


# add n of cells
make_new_df = False
if make_new_df:
    rows = []
    for ri, r in df_bkp.iterrows():
        # for n_sample in [35000, 250000, 500000, 750000, 1000000, 1250000, 1500000, 1750000, 2000000] + [None]:
        for n_sample in [None]:
            for n_epochs in (10, 20, 50, 100,): # 20, 50, 100): # 5, 10, 15, 20, 25):
                for n_layers in (3,):
                    for n_hidden in (256,):
                        from itertools import combinations
                        added = set()
                        for n_datasets in range(4, len(dataset_names) + 1):
                            # print(n_datasets)
                            for comb in combinations(set(dataset_names) - set(['Chen_a', 'Chen_b', 'Chen_c']), n_datasets):
                                # if ('Roska' in comb or 'Hackney' in comb) and len(comb) + 3 < 8:
                                #     continue
                                if 'Roska' in comb and 'Hackney' in comb: #  and len(comb) + 3 == 8:
                                    continue
                                if 'Hackney' in comb:
                                    continue
                                if len(comb) != 5:
                                    continue

                                k = '_'.join(sorted(comb))
                                print(k, comb)
                                if not k in added:
                                    added.add(k)
                                else:
                                    continue
                                # print(k)
                                # print(comb)

                                for n_cells_roska in [125000]: # range(0, 175001, 25000):
                                    rows.append(list(df_bkp.iloc[ri]) + [n_sample, n_epochs, comb, n_datasets + 3, n_cells_roska,
                                                                        n_layers, n_hidden] )
        break
    df = pd.DataFrame(rows, columns=list(df_bkp.columns) + ['n.sample', 'n.epochs', 'comb', 'n.datasets', 'n_cells_roska', 'n_layers', 'n_hideen'])
    # df['method'] = 'scanvi'
    df['cell_type_key'] = 'cell.type'


# In[19]:


df


# In[20]:


df.shape


# In[23]:


if make_new_df:
    for ri, r in df.iterrows():
        method, hvg, cell_type_key, input_path, output_path, in_exists, out_exists, n_sample, n_epochs, comb_add, n_datasets, n_cells_roska, n_layers, n_hidden = df.iloc[ri]
        k_add = "_".join(comb_add)
        output_path = output_path.replace('.h5ad', '_%s_%i_%s_NROSKA_%i_NEPOCHS_%i_NLAYERS_%i_NHIDDEN_%i.h5ad' % (str(n_sample), n_epochs, k_add, n_cells_roska, n_epochs, n_layers, n_hidden))
        print(exists(output_path), output_path)
    for ri, i in df.iterrows():
        for rj, j in df.iterrows():
            a, b = i['comb'], j['comb']
            if ri == rj:
                continue
            if len(a) == len(b) and len(set(a) - set(b)) == 0:
                print(a, b)


# In[24]:


print(df.shape)


# In[25]:


df


# In[27]:


# if a for loop is approved, make a loop with increasing samples of cells
import gc
gc.collect()
print('query', query)
# method, hvg, cell_type_key, input_path, output_path, in_exists, out_exists, n_sample, n_epochs, comb_add, n_datasets, n_cells_roska, n_layers, n_hidden = df.iloc[query]
method, hvg, cell_type_key, input_path, output_path, in_exists, out_exists = df.iloc[query]

n_epochs = 25
print(df.iloc[query])
print('# epochs', n_epochs)


# In[28]:


# df[pd.Series([len(s) for s in df['comb']]) == 3]


# In[30]:


# k_add = "_".join(sorted(comb_add))

# output_path = output_path.replace('.h5ad', '_%s_%i_%s_NROSKA_%i_NEPOCHS_%i_NLAYERS_%i_NHIDDEN_%i.h5ad' % (str(n_sample), n_epochs, k_add, n_cells_roska, n_epochs, n_layers, n_hidden))
# output_path = output_path.replace('scvi', 'scanvi')

print(exists(input_path), input_path)
print(exists(output_path), output_path)
print('')

embed_path = output_path.replace('.h5ad', '_embed.csv')
print(exists(embed_path), embed_path)

parent_directory = os.path.abspath(os.path.join(output_path, os.pardir))
# print(exists(parent_directory), parent_directory)
if not exists(parent_directory):
    os.makedirs(parent_directory)

if exists(output_path):
    print('this output file already exists. Modestly walking out...')
    sys.exit()

print('reading input...')
ad = sc.read_h5ad(input_path)
adata = ad


# In[26]:


# adata = adata[adata.obs.dataset.isin(set(comb_add)) | adata.obs.dataset.isin(set(['Chen_a','Chen_b', 'Chen_c'])),:]
# print(adata.shape)
# batch = 'batch_donor_dataset'

# # adata = adata[adata.obs.dataset.isin(set(list(adata.obs.dataset.value_counts().index))),:]
# gc.collect()

# if n_sample is not None:
#     import random
#     random.seed(500)
#     sel_names = pd.Series(adata.obs_names).sample(int(n_sample)).values
#     adata = adata[adata.obs_names.isin(sel_names),:]

    
# idx_roska = adata[(adata.obs['dataset'] == 'Roska')].obs_names
# idx_roska = pd.Series(idx_roska).sample(min(n_cells_roska, len(idx_roska)), random_state=500).values
# print(len(idx_roska))

# # downsample Roska
# adata = adata[((adata.obs['dataset'] == 'Roska') & adata.obs_names.isin(set(idx_roska))) | ~adata.obs['dataset'].str.contains('Roska'),:]


# In[92]:


import gc
gc.collect()


# In[ ]:


print('location of scripts...')
print(scIB.integration)


# In[156]:


print(adata.shape)

cell_type_key = 'cell.type'
batch = 'batch_donor_dataset'
n_epochs = n_epochs

integrated = None
# adata = scIB.integration.runScGen(adata, batch, labels)
if method == 'scvi':
    print('scVI...')
    integrated, trainer = scIB.integration.runScvi(adata, batch, n_epochs=n_epochs)
elif method == 'scgen':
    print('scgen')
    from tensorflow.python.client import device_lib
    devices = device_lib.list_local_devices()
    print('# of detected devices', len(devices))

    gpu_found = False
    device_gpu = '0'
    for di, device in enumerate(devices):
        if device.name.split(':')[1] == 'GPU':
            gpu_found = True
            device_gpu = str(di)
        else:
            if device.name.split(':')[1] == 'XLA_GPU' and not gpu_found:
                device_gpu = str(di)
        print(di, device.name)
    print('GPU device found', gpu_found, di)

    if not gpu_found:
        print('Maybe XLA_GPU but not GPU found. Check tensorflow version')
        # assert False

    print(di, device.name)
    batch = 'batch_donor_dataset'
    print('starting scgen')

    print('here...')
    integrated = scIB.integration.runScGen_v2_0_0(adata, batch, cell_type_key, epochs=n_epochs, device=device_gpu, verbose=1)
elif method == 'scanvi':
    print('scanvi')
    # scvi
    integrated = scIB.integration.runScanvi(adata, batch, cell_type_key, n_epochs_scVI=n_epochs, n_epochs_scANVI=15)
                                           # n_layers=n_layers, n_hidden=n_hidden)
    print ('about to write to output scANVI...')
    # assert False

from os.path import exists
if integrated is not None and not exists(output_path):
    sc.write(output_path, integrated)

sys.exit()

adata = integrated
result = 'embed'
method = 'scanvi'

print('Preparing dataset...')
if result == 'embed':
    reduce_data(adata, n_top_genes=adata.shape[1], neighbors=True,
                use_rep='X_emb', pca=False, umap=False)
elif result == 'full':
    sc.pp.filter_genes(adata, min_cells=1)
    reduce_data(adata, n_top_genes=adata.shape[1], neighbors=True,
                use_rep='X_pca', pca=True, umap=False)

print('after return')
# print(adata)
# Calculate embedding
if method.startswith('conos'):
    print('Calculating graph embedding...')
    sc.tl.draw_graph(adata, key_added_ext='graph')
    basis = 'draw_graph_graph'
    label = 'Graph'
else:
    print('Calculating UMAP...')
    sc.tl.umap(adata)
    basis = 'umap'
    label = 'UMAP'

print('done...')
import os
# Save embedding coordinates
print('Saving embedding coordinates...')
label = 'UMAP'
basis = 'umap'
adata.obs[label + '1'] = adata.obsm['X_' + basis][:, 0]
adata.obs[label + '2'] = adata.obsm['X_' + basis][:, 1]
coords = adata.obs[['cell.type', 'batch_donor_dataset', label + '1', label + '2' ]]
coords.to_csv(os.path.join(embed_path), index_label='CellID')


sc.set_figure_params(facecolor='white', dpi=150)
sc.pl.umap(adata, color=['cell.type', 'dataset'])
plt.savefig(output_path.replace('.h5ad', '.png'))
plt.close()

print(exists(output_path), output_path)

gc.collect()


# In[ ]:


# %matplotlib inline
# elbo_train_set = trainer.history["elbo_train_set"]
# elbo_test_set = trainer.history["elbo_test_set"]
# x = np.linspace(0, n_epochs, (len(elbo_train_set)))
# plt.plot(x, elbo_train_set, label="train")
# plt.plot(x, elbo_test_set, label="test")
# # plt.ylim(1500, 3000)
# plt.legend()


# In[ ]:


# print(integrated)
# print(trainer)


# In[ ]:


# print('done...')

