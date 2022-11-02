#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import scanpy as sc
x=sc.read(f)

import sys
if 'X_umap' not in x.obsm:
	print('Error: X_umap is missing. See scanpy.tl.umap()')
	sys.exit(-1)

sc.set_figure_params(dpi_save=500, figsize=(width, height))

for splitby in label:
	if splitby not in x.obs_keys():
		print(f'Error: {splitby} is not a metadata.')
		sys.exit(-1)

	ncolor=len(x.obs[splitby].value_counts())
	if ncolor<100:
		sc.pl.umap(x, color=splitby, frameon=False, show=False, save=f'{bname}_umap_{splitby}.png')
		sc.pl.umap(x, color=splitby, frameon=False, show=False, save=f'{bname}_umap_{splitby}_ondata.png'
			, legend_loc='on data', legend_fontsize='xx-small', legend_fontweight='normal'
			)
	else:
		import seaborn as sns
		palette=sns.husl_palette(ncolor)
		sc.pl.umap(x, color=splitby, palette=palette, frameon=False, show=False, save=f'{bname}_umap_{splitby}.png')
		sc.pl.umap(x, color=splitby, palette=palette, frameon=False, show=False, save=f'{bname}_umap_{splitby}_ondata.png'
			, legend_loc='on data', legend_fontsize='xx-small', legend_fontweight='normal'
			)
