library("DESeq2")
library("ggplot2")
library( "gplots" )
library( "RColorBrewer" )
library( "genefilter" )
library("ggrepel")
library(tidyr)
library(peer)
args <- commandArgs(trailingOnly = TRUE)
dirIn=paste0("/storage/chenlab/Users/junwang/human_meta/data/age_DESeq2_75_age_interval_batch/",args[1])

dir.create(dirIn,recursive = TRUE)
setwd(dirIn)
dirIn <- getwd()
exp=read.table(paste0("/storage/chenlab/Users/junwang/human_meta/data/genexp_donor_cell_raw_batch_new/exp_",args[1]),header=T)
file_info=read.table("/storage/chenlab/Users/junwang/human_meta/data/atlasrna_metadata_chen_batch",header=T)
m=match(file_info$sampleid,colnames(exp),nomatch=0)
exp=exp[,m]
fListNames=colnames(exp)
m=match(fListNames,file_info$sampleid)
file_info$age_interval = "53_65"
file_info[file_info$age>65&file_info$age<=70,]$age_interval="66_70"
file_info[file_info$age>70&file_info$age<=75,]$age_interval="71_75"
file_info[file_info$age>75&file_info$age<=80,]$age_interval="76_80"
file_info[file_info$age>80&file_info$age<=85,]$age_interval="81_85"
file_info[file_info$age>85&file_info$age<=91,]$age_interval="86_91"

seqProfile=exp

#######compute peer factor
#vst= varianceStabilizingTransformation(dds2)
#exp_vst = assay(vst)  
#model = PEER()
#PEER_setPhenoMean(model,as.matrix(t(exp_vst)))
#dim(PEER_getPhenoMean(model))
#PEER_setNk(model,3) #2 factor
#PEER_getNk(model)
#PEER_update(model)
#factors = PEER_getX(model)
#dim(factors)
#weights = PEER_getW(model)
#dim(weights)
#precision = PEER_getAlpha(model)
#dim(precision)
#residuals = PEER_getResiduals(model)
#dim(residuals)
#plot(precision)
#PEER_setAdd_mean(model, TRUE)
#rownames(factors)=colnames(exp_vst)
#write.table(factors,paste0("vst_3peer"),sep="\t",quote=F)

##########
Design=data.frame(row.names=file_info[m,]$sampleid,age=as.numeric(file_info[m,]$age),gender=file_info[m,]$gender,race=file_info[m,]$race,age_interval=file_info[m,]$age_interval,batch=file_info[m,]$batch)
Design$age=scale(Design$age,center=T)
#dds    <- DESeqDataSetFromMatrix(countData = exp,colData = Design , design = ~gender+race+peer1+age_interval)
dds    <- DESeqDataSetFromMatrix(countData = exp,colData = Design , design = ~gender+race+batch+age_interval)

#dds    <- DESeqDataSetFromMatrix(countData = exp,colData = Design , design = ~gender+race+age_interval)
#dds    <- DESeqDataSetFromMatrix(countData = exp,colData = Design , design = ~age_interval)


#keep <- rowSums(counts(dds)) >= 10
keep <- rowMeans(counts(dds)) >= 10

dds2 = dds[keep,]
dds2$age_interval <- as.numeric(factor(dds2$age_interval, levels=c("53_65","66_70","71_75","76_80","81_85","86_91")))
#dds2$age_interval <- factor(dds2$age_interval, levels=c("53_65","66_70","71_75","76_80","81_85","86_91"))
#design(dds2) = formula(~gender+race+batch+age_interval)
#dds2$age = factor(dds2$age, levels=seq(50,95,1))
#dds2$condition <- relevel(dds$age_interval, ref=refConditionSample)
#dds2           <- DESeq(dds2,test="LRT",reduced=~gender+race+batch)
#dds2           <- DESeq(dds2,test="LRT",reduced=~gender+race+peer1)
dds2           <- DESeq(dds2,test="LRT",reduced=~gender+race+batch)
#dds2           <- DESeq(dds2) #,test="LRT")

res               <- results(dds2)
summary(res)

finName     <- "MA"
foutPlotpdf <- paste("1_plot_", finName,"_",args[1], ".pdf", sep="")
cat("Plotting a MA plot.", "\n", sep="")
titlePlot <- "MA plot"
pdf(foutPlotpdf)
plotMA(res, main= titlePlot, ylim=c(-2,2))
dev.off()

cat("Plotting a MA plot.", "\n", sep="")
foutPlotHist <- paste("2_plot_histogram_pval_",args[1],".pdf", sep="")
pdf(foutPlotHist)
hist( res$pvalue, breaks=20, col="grey" )
dev.off()

resOrdered        <- res[order(res$padj),]
colNameResOrdered <- as.character(colnames(resOrdered))
rowNameResordered <- as.character(rownames(resOrdered))
reorderedTable    <- data.frame(rowNameResordered,resOrdered)

fout1 <- paste0(args[1],"_RNAseq_profile_raw_bulk.txt")
fout2 <- paste0(args[1],"_DEGs_bulk.txt")
cat("Writing the output.", "\n", sep="")
write.table(seqProfile, fout1, sep="\t", col.names=T, row.names=T, quote=F )
write.table(reorderedTable, fout2, sep="\t", col.names=T, row.names=F, quote=F )

rld <- rlog( dds2 )
head( assay(rld) )
#vst <- varianceStabilizingTransformation( dds2 )
#head( assay(vst) )

cat("Plotting a scatter plot.", "\n", sep="")
foutPlotScatterA <- paste("3_plot_scatter_",args[1],".pdf", sep="")
pdf(foutPlotScatterA)
par( mfrow = c( 1, 2 ) )
plot( log2( 1+counts(dds2, normalized=TRUE)[, 1:2] ), col="#00000020", pch=20, cex=0.3 )
plot( assay(rld)[, 1:2], col="#00000020", pch=20, cex=0.3 )
#plot( assay(vst)[, 1:2], col="#00000020", pch=20, cex=0.3 )

dev.off()

panel.cor <- function(x, y, digits=2, prefix="", cex.cor)
{
    usr <- par("usr"); on.exit(par(usr))
    par(usr = c(0, 1, 0, 1))
    r <- abs(cor(x, y))
    txt <- format(c(r, 0.123456789), digits=digits)[1]
    txt <- paste(prefix, txt, sep="")
    if(missing(cex.cor)) cex <- 0.8/strwidth(txt)

    test <- cor.test(x,y)
    Signif <- symnum(test$p.value, corr = FALSE, na = FALSE,
                  cutpoints = c(0, 0.001, 0.01, 0.05, 0.1, 1),
                  symbols = c("***", "**", "*", ".", " "))
     text(0.5, 0.5, txt, cex = cex)
    text(.8, .8, Signif, cex=cex, col=2)
}
#colnames(vst) <- fListNames
#vstExp <- assay(vst)

colnames(rld) <- fListNames
rldExp <- assay(rld)
########cat("Plotting a paired plot.", "\n", sep="")
#######foutPlotPairs <- paste("4_plot_Pairs", ".pdf", sep="")
########pdf(foutPlotPairs)
#pairs(vstExp, lower.panel=panel.smooth, upper.panel=panel.cor)

###########pairs(rldExp, lower.panel=panel.smooth, upper.panel=panel.cor)
###########dev.off()

# H-clusting
sampleDists <- dist( t( assay(rld) ) )
sampleDists

sampleDistMatrix           <- as.matrix( sampleDists )
rownames(sampleDistMatrix) <- fListNames  #paste( rld$treatment,rld$patient, sep="-" )
colnames(sampleDistMatrix) <- fListNames

library( "gplots" )
library( "RColorBrewer" )
colours = colorRampPalette( rev(brewer.pal(9, "Blues")) )(255)
cat("Plotting a H-clust plot.", "\n", sep="")
foutPlotHclust <- paste("5_plot_Hcluster_",args[1], ".pdf", sep="")
#setwd(dirOut)
pdf(foutPlotHclust)
par(oma=c(3,4,4,2))
heatmap.2( sampleDistMatrix, trace="none", cexRow=0.7,cexCol=0.7)

#heatmap.2( sampleDistMatrix, trace="none", cexRow=0.7,cexCol=0.7, col=colours)
dev.off()
write.table(sampleDistMatrix,file="HC_matrix",sep="\t",quote=F,row.names=T)
write.table(assay(rld),file="rld",sep="\t",quote=F,row.names=T)
# PCA
cat("Plotting a PCA plot.", "\n", sep="")
foutPlotPCA <- paste("6_plot_PCA", ".pdf", sep="")
#setwd(dirOut)
pdf(foutPlotPCA)
print(plotPCA(rld, intgroup=c("age")))
#print(plotPCA(vst, intgroup=c("age")))

dev.off()


data1=reorderedTable
data1$diff_exp="Not Significant"
data1[(!is.na(data1$padj))&(data1$padj<0.01),]$diff_exp="Padj<0.01"
#data1[(!is.na(data1$padj))&(data1$padj<0.01)&((data1$log2FoldChange<=-1)|(data1$log2FoldChange>=1)),]$diff_exp="Padj<0.01&|log2FC|>=1"
data1[(!is.na(data1$padj))&(data1$padj<0.01)&((data1$log2FoldChange<=-0.5)|(data1$log2FoldChange>=0.5)),]$diff_exp="Padj<0.01&|log2FC|>=0.5"

data1$label=NA
 pdf(paste0("7_vocano_plot_",args[1],".pdf"),width=10,height=8)
p= ggplot(data=data1, aes(x=log2FoldChange, y=-log10(padj),color=as.factor(diff_exp),label=label)) +geom_point() + theme_minimal() +geom_text_repel(box.padding = 0.5, max.overlaps = Inf)+ scale_color_manual(values=c("black", "blue", "red"))+labs(color="Differential expression")+theme(text = element_text(size=20),panel.background=element_blank(),panel.grid.major=element_blank(),panel.grid.minor=element_blank(), panel.border=element_blank(),axis.line=element_line(colour="black"))
print(p)
dev.off()
