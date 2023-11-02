import anndata
import numpy as np
import scanpy as sc
from os.path import join, exists
import gc

def get_datasets(names, code_n_cells=''):
    adatas = []
    bydataset_directory = '../../data/integration_march_2021/input/bydataset%s' % code_n_cells
    for f in names: # listdir(bydataset_directory):
        # if 'Chen' in f:
        #     continue
        f = f + code_n_cells + '.h5ad'
        print(f)
        p = join(bydataset_directory, f)
        print(p)
        
        if not exists(p):
            continue
        
        ad = sc.read(p, cache=True)
        ad.obs['cell.type'] = 'unassigned' if not 'scpred_prediction' in ad.obs else ad.obs['scpred_prediction']

        # ad.layers['counts'] = ad.layers['counts'].astype('float32')
        # print(type(ad.layers['counts']), ad.layers['counts'].dtype)
        
        # this is a rough filter to remove cells with less than 500 cells per batch, if existing.
        nCount_RNA_thr = 500
        ad = ad[ad.obs['nCount_RNA'] > nCount_RNA_thr,:]
        
        # do gc
        gc.collect()
            
        # we need to filter genes individually, because in the biggest dataset this does not work (memory)
        min_cells = 50
        print('after loading', ad.shape)
        print('filtering by number of min_cells with gene')
        if False:
            # we need to filter genes individually, because in the biggest dataset this does not work (memory)
            gene_mask = np.count_nonzero(ad.X.astype('bool').toarray(), axis=0) > min_cells
            ad = ad[:,gene_mask]
        else:
            sc.pp.filter_genes(ad, min_cells=min_cells)
        print('after', ad.shape)
        gc.collect()        
        # print('updating names....')
        ad.obs.index = ad.obs.index + ':' + ad.obs['dataset'].astype(str) + ':' + ad.obs['batch'].astype(str)
        
        # print values per dataset
        # print(ad.obs.dataset.value_counts())
        
        ad_not_ok = ad[~ad.obs.dataset.isin(set(names)),:]
        if ad_not_ok.shape[0] > 0:
            print('# problem with dataset. Other datasets found')
            # print(ad_not_ok.obs.dataset.value_counts())
            assert False
        

        ad = ad[ad.obs.dataset.isin(set(names)),:]
        
        if ad.raw is not None:
            del ad.raw
        
        adatas.append(ad)
        
    print('objects before concatenation')
    for ai, ad in enumerate(adatas):
        pass
        # print(ai)
        # print(ad)
        # print(ad.obs.index)
        # print(ad.obs.index.value_counts())

    print('concatenating...')
    ad = anndata.concat(adatas)
    
    if ad.raw is not None:
        del ad.raw
    
    print('names upon integration')
    print(ad.obs.index)
    return ad
