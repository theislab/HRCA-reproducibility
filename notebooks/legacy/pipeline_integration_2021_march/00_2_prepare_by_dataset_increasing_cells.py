import warnings
warnings.filterwarnings("ignore")
import os
import scanpy as sc
from os.path import join
from os import listdir
import anndata
import numpy as np
import scipy

# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    print('{:.3} MB'.format(x.__sizeof__()/1e6))

### Use the scran related directory to map all the files we need to put together.
datadir_orig = '/storage/groups/ml01/datasets/projects/20210318_retinal_data_integration_ignacio.ibarra_malte.luecken'
datadir_scran = '/mnt/znas/icb_zstore01/groups/ml01/workspace/ignacio.ibarra/theislab/retinal_scRNAseq_integration/data/integration_march_2021/scran'
filenames = [f for f in os.listdir(datadir_orig)]
filenames_md5 = [f.strip() for f in open(os.path.join(datadir_orig, 'md5sum.txt'))]

files = set()
for qi in filenames_md5:
    md5, fi = qi.split('  ')
    # print(fi)
    found = os.path.exists(os.path.join(datadir_scran, fi))
    if not found:
        print('not found', fi)
    files.add(fi)

filenames_by_dataset = {}
for f in filenames_md5:
    dataset, filename = f.split(' ')[-1].split('/')[-2:]
    if not dataset in filenames_by_dataset:
        filenames_by_dataset[dataset] = []
    filenames_by_dataset[dataset].append(filename)

# get all files from a single directory
def get_by_dataset(dataset_name, filenames=None, n_sample=None):
    adatas = []
    
    if (filenames is None):
        filenames = [f for f in listdir(join(datadir_scran, dataset_name))]
    print('# datasets', len(filenames))
    for f in filenames:
        if len(adatas) % 20 == 0:
            print('loaded so far', len(adatas))
        p = join(datadir_scran, dataset_name, f)
        print(p)
        ad = sc.read_h5ad(p)
        
        if n_sample is not None:
            idx_sample = ad.obs.sample(n_sample if n_sample < ad.shape[0] else ad.shape[0]).index
            ad = ad[ad.obs.index.isin(idx_sample),:]
            # print(ad.shape)        
        
        ad.obs['dataset'] = dataset_name
        ad.obs['filename'] = f.replace('.h5ad', '')
        adatas.append(ad)
    return adatas[0].concatenate(adatas[1:]) # join='outer')

from os.path import exists
for n_sample in [250, 500, 1000, None]:
    for dataset in filenames_by_dataset:
        print(dataset)

        subsampling_code = ('_' + str(n_sample) if n_sample is not None else '')
        next_filename = '%s%s.h5ad' % (dataset, subsampling_code)
        outdir = '../../data/integration_march_2021/input/bydataset%s' % subsampling_code
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