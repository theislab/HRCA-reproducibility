#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
if __name__ == '__main__':
	import scanpy as sc
	x=sc.read(f)
	sc.tl.rank_genes_groups(x, groupby=groupby, use_raw=raw, n_genes=ngene, method='wilcoxon')

	if '_index' in x.var_keys():
		x.var.set_index('_index', inplace=True)

	if x.raw is not None:
		x.__dict__['_raw'].__dict__['_var']=x.__dict__['_raw'].__dict__['_var'].rename(columns={'_index': 'features'})

	sc.write(filename=f'{bname}.h5ad', adata=x)
	x.obs['barcode']=x.obs.index
	x.obs.to_csv(f'{bname}_obs.txt.gz', sep='\t', index=False)
	x.var['symbol']=x.var.index
	x.var.to_csv(f'{bname}_var.txt.gz', sep='\t', index=False)
