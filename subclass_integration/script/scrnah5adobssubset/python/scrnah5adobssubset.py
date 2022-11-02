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

	if invert:
		setobs=set(obss)
		obss=[k for k in x.obs_keys() if k not in setobs]

	# bug fix: subseting x.obs by obss
	x.obs=x.obs.loc[:, x.obs.columns.isin(obss)]
	sc.write(filename=f'{outdir}/{bname}.h5ad', adata=x)

	x.obs['barcode']=x.obs.index
	x.obs.to_csv(f'{outdir}/{bname}_obs.txt.gz', sep='\t', index=False)
	x.var['symbol']=x.var.index
	x.var.to_csv(f'{outdir}/{bname}_var.txt.gz', sep='\t', index=False)
