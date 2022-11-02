#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

if __name__ == '__main__':
	import scanpy as sc
	if f.endswith('.h5ad'):
		x=sc.read(f)
	else:
		print("Error: please input .h5ad file.")
		import sys
		sys.exit(-1)

	# bug fix the int columns
	if x.obs[label].dtype==int:
		x.obs[label]=x.obs[label].astype(str)

	if invert:
		x=x[~x.obs[label].isin(values)].copy()
	else:
		x=x[x.obs[label].isin(values)].copy()

	## Bug fix
	if '_index' in x.var_keys():
		x.var.set_index('_index', inplace=True)
	if x.raw is not None:
		if '_index' in x.__dict__['_raw'].__dict__['_var']:
			x.__dict__['_raw'].__dict__['_var'].set_index('_index', inplace=True)

	if raw:
		import anndata
		if len(obss)>0:
			x=anndata.AnnData(X=x.raw.X, obs=x.obs[obss], var=x.var.index)
		else:
			x=anndata.AnnData(X=x.raw.X, obs=x.obs, var=x.var)

	sc.write(filename=f'{bname}.h5ad', adata=x)
	x.obs['barcode']=x.obs.index
	x.obs.to_csv(f'{bname}_obs.txt.gz', sep='\t', index=False)
	x.var['symbol']=x.var.index
	x.var.to_csv(f'{bname}_var.txt.gz', sep='\t', index=False)
