#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import sys
import scanpy as sc
if __name__ == '__main__':
	x=sc.read(f)
	if raw:
		x=x.raw.to_adata()
	if norm:
		sc.pp.normalize_total(x)
		sc.pp.log1p(x)

	x.var['mito']=x.var_names.str.startswith(('mt-', 'MT-'))
	sc.pp.calculate_qc_metrics(x, qc_vars=['mito'], inplace=True)

	obskeys=['n_genes_by_counts'
		, 'log1p_n_genes_by_counts'
		, 'total_counts'
		, 'log1p_total_counts'
		, 'pct_counts_in_top_50_genes'
		, 'pct_counts_in_top_100_genes'
		, 'pct_counts_in_top_200_genes'
		, 'pct_counts_in_top_500_genes'
		, 'total_counts_mito'
		, 'log1p_total_counts_mito'
		, 'pct_counts_mito'
		]

	sc.set_figure_params(dpi_save=500, figsize=(width, height))
	for key in obskeys:
		if key not in x.obs_keys():
			print(f'Error: {key} is not observed')
			sys.exit(-1)
		sc.pl.violin(x, keys=[key], groupby=groupby, use_raw=False, stripplot=False, rotation=angle, show=False, xlabel=groupby, save=f'{bname}_{key}.png')
	for key in keys:
		sc.pl.violin(x, keys=[key], groupby=groupby, use_raw=False, stripplot=False, rotation=angle, show=False, xlabel=groupby, save=f'{bname}_{key}.png')
