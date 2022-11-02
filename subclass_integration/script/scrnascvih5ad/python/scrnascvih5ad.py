#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import scanpy as sc
x=sc.read(f)
x.var_names_make_unique()
print(vars(x))

x.layers['hvgcounts']=x.X.copy()
sc.pp.normalize_total(x)
sc.pp.log1p(x)
x.raw=x
sc.pp.highly_variable_genes(
	x
	, flavor=flavor
	, n_top_genes=ntop
	, subset=True
	, layer='hvgcounts'
	, batch_key=batchkey
)

import scvi
scvi.model.SCVI.setup_anndata(x, layer='hvgcounts', batch_key=batchkey)
vae=scvi.model.SCVI(x, n_layers=nlayer, n_latent=nlatent)
vae.train(max_epochs=epoch)
vae.save(f'{bname}_model')
x.obsm['X_scVI']=vae.get_latent_representation()
if normcounts:
	import anndata
	denoised=anndata.AnnData(X=vae.get_normalized_expression(), obs=x.obs)
	sc.write(filename=f'{bname}_denoised.h5ad', adata=denoised)

sc.pp.neighbors(x, use_rep='X_scVI', random_state=seed)
sc.tl.leiden(x, resolution=1, random_state=seed)
sc.tl.umap(x, random_state=seed)

sc.set_figure_params(dpi_save=500, figsize=(5, 5))
for splitby in [batchkey, 'leiden']:
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

print(dir(x))
print(vars(x))
sc.write(filename=f'{bname}.h5ad', adata=x)
x.obs['barcode']=x.obs.index
x.obs.to_csv(f'{bname}_obs.txt.gz', sep='\t', index=False)
x.var['symbol']=x.var.index
x.var.to_csv(f'{bname}_var.txt.gz', sep='\t', index=False)
