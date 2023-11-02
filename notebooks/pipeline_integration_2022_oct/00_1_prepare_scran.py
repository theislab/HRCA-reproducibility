#!/usr/bin/env python
# coding: utf-8

# ### 1. Verify that all data reported by Jin is in

# In[24]:


import scIB


# In[25]:


import os
import scanpy as sc
from os.path import join
from os import listdir
import anndata
import numpy as np
import scipy
import os


# In[26]:


# convert counts into float32
# Convenience method for computing the size of objects
def print_size_in_MB(x):
    print('{:.3} MB'.format(x.__sizeof__()/1e6))


# In[27]:


# datadir = '/storage/groups/ml01/datasets/projects/20210318_retinal_data_integration_ignacio.ibarra_malte.luecken'
datadir = '/mnt/f/workspace/theislab/retina/data/RNA'
# outdir = '/mnt/znas/icb_zstore01/groups/ml01/workspace/ignacio.ibarra/theislab/retinal_scRNAseq_integration/data/integration_march_2021/scran'
outdir = '/mnt/f/workspace/theislab/retina/data/integration_oct_2022/scran'
os.path.exists(outdir), os.path.exists(datadir)


# In[28]:


filenames = [f for f in os.listdir(datadir)]


# In[29]:


# filenames_md5 = [f.strip() for f in open(os.path.join(datadir, 'md5sum.txt'))]
filenames_md5 = [f.strip() for f in os.listdir(datadir) if f.endswith(".h5ad")]
filenames_md5

# files = set()
# for qi in filenames_md5:
#     md5, fi = qi.split('  ')
#     found = os.path.exists(os.path.join(datadir, fi))
#     if not found:
#         print('not found', fi)
#     files.add(fi)


# **The following files are listed but for some reason not found anymore. Consider deleting (Request to Jin first)**

# In[30]:


filenames_by_dataset = {}
for f in filenames_md5:
    # dataset, filename = f.split(' ')[-1].split('/')[-2:]
    dataset = f.split('_')[0] if not "Chen" in f else f.split('_')[0] + '_' + f.split('_')[1]
    filename = f
    print(dataset, filename)
    if not dataset in filenames_by_dataset:
        filenames_by_dataset[dataset] = []
    filenames_by_dataset[dataset].append(filename)


# ### scran normalization

# In[31]:


path_preprocessing = '/mnt/c/Users/ignacio.ibarra/Dropbox/workspace/theislab/HECA-scib-pipeline/scripts/preprocessing.py'
os.path.exists(path_preprocessing)


# In[32]:


def execute_preprocessing(input_path, output_path):
    print('')
    path_preprocessing = '/mnt/c/Users/ignacio.ibarra/Dropbox/workspace/theislab/HECA-scib-pipeline/scripts/preprocessing.py'
    cmd = 'python %s -i %s -o %s' % (path_preprocessing, input_path, output_path)
    
    try:
        print(cmd)
        os.system(cmd)
    except Exception as err:
        print('something went wrong...')
        print(err)


# In[33]:


import multiprocessing
from multiprocessing import Process
from multiprocessing import Manager

def run(function, input_list, n_cores, log_each=None, log=False):
    print(('run function %s with n_cores = %i' % (function, n_cores)))
    print(function)
    # print 'with input list of len'
    # print len(input_list)
    # print 'in groups of %d threads' % n_threads

    assert n_cores <= 20

    # the type of input_list has to be a list. If not
    # then it can a single element list and we cast it to list.
    if not isinstance(type(input_list[0]), type(list)):
        input_list = [[i] for i in input_list]

    n_groups = int(len(input_list) / n_cores + 1)
    # print 'n groups', n_groups

    n_done = 0
    for group_i in range(n_groups):
        start, end = group_i * n_cores, (group_i + 1) * n_cores
        # print 'start', start, 'end', end

        threads = [None] * (end - start)
        for i, pi in enumerate(range(start, min(end, len(input_list)))):
            next_args = input_list[pi]
            if log:
                print(next_args)
            # print next_kmer
            threads[i] = Process(target=function, args=next_args)
            # print 'starting process #', i
            threads[i].start()

        # print  threads
        # print 'joining threads...'
        # do some other stuff
        for i in range(len(threads)):
            if threads[i] is None:
                continue
            threads[i].join()

            n_done += 1
            if log_each is not None and log_each % n_done == 0:
                print('Done %i so far' % n_done)
    print('done...')


# In[34]:


from os.path import join
arguments = []

for dataset in filenames_by_dataset:
    # print(dataset)
    for filename in filenames_by_dataset[dataset]:
        input_file = join(datadir, filename)
        next_outdir = join(outdir, dataset)
        # print(next_outdir)
        
        if not os.path.exists(next_outdir):
            os.mkdir(next_outdir)
            
        output_file = join(next_outdir, filename)

        # print(os.path.exists(output_file), output_file)
        if os.path.exists(output_file):
            # print(os.path.exists(output_file), 'skip...')
            continue
        
        # print(input_file)
        # print(output_file)
        # print('')
        
        arguments.append([input_file, output_file])
        # ad = sc.read_h5ad(join(datadir, p))
    


# In[35]:


arguments


# In[36]:


# this is a test. maintain commented after finishing
# !python ../../scib/scripts/preprocessing_remove_empty.py -i /storage/groups/ml01/datasets/projects/20210318_retinal_data_integration_ignacio.ibarra_malte.luecken/Wong/Retina_2B.h5ad -o /mnt/znas/icb_zstore01/groups/ml01/workspace/ignacio.ibarra/theislab/retinal_scRNAseq_integration/data/integration_march_2021/scran/Wong/Retina_2B.h5ad


# In[37]:


print(len(arguments))
arguments = sorted(arguments, key=lambda x: os.path.getsize(x[0]))


# In[23]:


run(execute_preprocessing, arguments, n_cores=1)

