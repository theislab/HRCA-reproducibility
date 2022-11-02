#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import scanpy as sc
import pandas as pd

if __name__ == '__main__':
	x=sc.read(f)
	if raw:
		x=x.raw.to_adata()
	if norm:
		sc.pp.normalize_total(x)
		sc.pp.log1p(x)

	print('==> x.var.index')
	print(x.var.index)

	marker=pd.read_csv(marker, sep='\t', header=None)
	print('==> marker')
	print(marker)

	if marker.shape[1]==2:
		marker=marker[marker[1].isin(x.var.index)]
		marker=marker.groupby(0).apply(lambda x: x[1].tolist()).to_dict()
	else:
		marker=marker[0]
		marker=marker[marker.isin(x.var.index)]
	print('==> marker subset')
	print(marker)

	sc.set_figure_params(dpi_save=500, figsize=(width, height))
	sc.pl.stacked_violin(x, marker, groupby=groupby, use_raw=False, dendrogram=dendrogram, log=log, stripplot=False, swap_axes=False, show=False, title=groupby, save=f'{bname}.png')

	if save:
		sc.write(filename=f'{bname}.h5ad', adata=x)
		x.obs['barcode']=x.obs.index
		x.obs.to_csv(f'{bname}_obs.txt.gz', sep='\t', index=False)
		x.var['symbol']=x.var.index
		x.var.to_csv(f'{bname}_var.txt.gz', sep='\t', index=False)
