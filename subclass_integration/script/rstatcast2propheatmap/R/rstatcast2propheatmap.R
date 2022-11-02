# vim: set noexpandtab tabstop=2:

suppressPackageStartupMessages(library(jlutils))
f=read.txt('stdin', header=T)
rownames(f)=f$x
f$x=NULL
str(f)
write.txt(cbind(x=rownames(f), f), file=sprintf('%s/%s_count.txt.gz', outdir, bname))

prob=sweep(f, 2, colSums(f), '/')
str(prob)
write.txt(cbind(x=rownames(prob), prob), file=sprintf('%s/%s_prob.txt.gz', outdir, bname))

lower=min(prob)
upper=round(max(prob), 2)
suppressPackageStartupMessages(library(pheatmap))
pdf(sprintf('%s/%s_heatmap.pdf', outdir, bname), width=width, height=height)
x=pheatmap(prob
	, color=colorRampPalette(c('white', 'red'))(1024)
	, breaks=seq(lower, upper, length.out=1024)
	, legend_breaks=c(lower, upper)
	, legend_labels=c(lower, upper)
	, show_rownames=T
	, show_colnames=T
	, cluster_rows=F
	, cluster_cols=F
	, display_numbers=F
	, fontsize=size
	, fontsize_number=size
	, angle_col=angle
	)
dev.off()
