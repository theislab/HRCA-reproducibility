#!/usr/bin/env python3
# vim: set noexpandtab tabstop=2 shiftwidth=2 softtabstop=-1 fileencoding=utf-8:

import scanpy as sc
x=sc.read(f)
if use=='raw':
	X=x.raw.X
else:
	X=x.X

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import SCCAF as sf
y_prob, y_pred, y_test, clf, cvsm, acc=sf.SCCAF_assessment(X, x.obs[clusterlabel], n=ncell, random_state=seed, n_jobs=numthreads)
plt.figure(figsize=(5, 5), dpi=500)
sf.plot_roc(y_prob, y_test, clf, cvsm=cvsm, acc=acc)
plt.savefig(f'{bname}_roc_init.png')
plt.close()

from matplotlib.backends.backend_pdf import PdfPages
backend=PdfPages(f'{bname}_optimize.pdf')
x.obs['L1_Round0']=x.obs[clusterlabel]
sf.SCCAF_optimize_all(ad=x, min_acc=minacc, use=use, plot_dist=plot, plot_cmat=plot, n=ncell, n_jobs=numthreads, mplotlib_backend=backend)
backend.close()
sc.write(filename=f'{bname}.h5ad', adata=x)

import re
def extract_round_number(text):
    '''
    Obtain round number from the label so that it can be used for sorting rounds (specifying key).
    '''
    round_num=re.sub(r'.*_Round(\d+)$', r'\1', text)
    return int(round_num) if round_num.isdigit() else round_num

rounds=[]
for round_key in x.obs_keys():
	if re.match(r'L1_Round\d+$', round_key):
		rounds.append(round_key)
rounds.sort(key=extract_round_number)
with open(f'{bname}_rounds.txt', 'w') as f:
	for item in rounds:
		f.write("%s\n" % item)

y_prob, y_pred, y_test, clf, cvsm, acc=sf.SCCAF_assessment(X, x.obs['L1_result'], n=ncell, random_state=seed, n_jobs=numthreads)
plt.figure(figsize=(5, 5), dpi=500)
sf.plot_roc(y_prob, y_test, clf, cvsm=cvsm, acc=acc)
plt.savefig(f'{bname}_roc_optimize.png')
plt.close()

x.obs['barcode']=x.obs.index
x.obs.to_csv(f'{bname}_obs.txt.gz', sep='\t', index=False)
x.var['symbol']=x.var.index
x.var.to_csv(f'{bname}_var.txt.gz', sep='\t', index=False)
