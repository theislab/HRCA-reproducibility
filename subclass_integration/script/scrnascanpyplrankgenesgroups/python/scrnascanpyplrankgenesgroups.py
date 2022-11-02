#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

if __name__ == '__main__':
	import scanpy as sc
	x=sc.read(infile)
	sc.set_figure_params(dpi_save=500)
	sc.pl.rank_genes_groups(x, n_genes=ngene, show=False, save=f'{bname}.png', figsize=(width, height))
	if len(groups)==0:
		groups=x.uns['rank_genes_groups']['names'].dtype.names
	for g in groups:
		sc.pl.rank_genes_groups(x, groups=[g], n_genes=ngene, show=False, save=f'{bname}_{g}.png', figsize=(width, height))
