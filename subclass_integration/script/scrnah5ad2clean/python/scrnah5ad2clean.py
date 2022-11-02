#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import os
import sys
import scanpy as sc
import anndata as ad
import pandas as pd

if f.endswith('.h5ad'):
	x=sc.read(f)
else:
	print("Error: please input .h5ad file.")
	sys.exit(-1)

if '_index' in x.var_keys():
	x.var.set_index('_index', inplace=True)
if x.raw is not None:
	if '_index' in x.__dict__['_raw'].__dict__['_var']:
		x.__dict__['_raw'].__dict__['_var'].set_index('_index', inplace=True)

var=x.var
if varindex:
	var=pd.DataFrame(index=x.var.index)

obs=x.obs
if len(obss)>0:
	obs=x.obs[obss]

if layers:
	if key!='':
		tmp=ad.AnnData(X=x.layers[key], obs=obs, var=var)
	else:
		tmp=ad.AnnData(X=x.X, obs=obs, var=var, layers=layers)
elif raw:
	tmp=ad.AnnData(X=x.raw.X, obs=obs, var=var)
else:
	tmp=ad.AnnData(X=x.X, obs=obs, var=var)

# add obsm
if fullobsm:
	obsms=x.obsm_keys()
if len(obsms)>0:
	for obsm in obsms:
		tmp.obsm[obsm]=x.obsm[obsm]

x=tmp
sc.write(filename=f'{outdir}/{bname}.h5ad', adata=x)
x.obs['barcode']=x.obs.index
x.obs.to_csv(f'{outdir}/{bname}_obs.txt.gz', sep='\t', index=False)
x.var['symbol']=x.var.index
x.var.to_csv(f'{outdir}/{bname}_var.txt.gz', sep='\t', index=False)
