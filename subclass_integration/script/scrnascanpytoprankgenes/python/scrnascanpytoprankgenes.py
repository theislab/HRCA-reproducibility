#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

if __name__ == '__main__':
	import scanpy as sc
	x=sc.read(f)

	if 'rank_genes_groups' in x.uns:
		if len(groups)==0:
			groups=x.uns['rank_genes_groups']['names'].dtype.names

		import pandas as pd
		header=['names', 'logfoldchanges', 'pvals', 'pvals_adj', 'scores']
		for g in groups:
			result=pd.concat(
				[pd.DataFrame(x.uns['rank_genes_groups'][h])[g].head(ntop) for h in header]
				, axis=1
				, keys=header
				)
			result.to_csv(f'{bname}_rankgene_g{g}_n{ntop}.txt.gz', sep='\t', index=False)
	else:
		import sys
		print("Error: rank_genes_groups is missing in x.uns. See `scrnascanpyplrankgenesgroups.sh`.")
		sys.exit(-1)
