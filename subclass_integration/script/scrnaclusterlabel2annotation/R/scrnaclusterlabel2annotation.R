# vim: set noexpandtab tabstop=2:

suppressPackageStartupMessages(library(jlutils))
x=read.txt(infile, header=T)
xx=x[, -seq_len(skip_cols), drop=F]
anno_labels=names(xx)
celltype=apply(xx>=count
	, 1
	, function(xr) {
		paste(anno_labels[xr], collapse='+')
	})
write.txt(cbind(x, celltype), file=sprintf('%s/%s.txt.gz', outdir, bname))
