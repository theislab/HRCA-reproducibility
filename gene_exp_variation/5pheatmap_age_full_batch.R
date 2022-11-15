library("DESeq2")
library("ggplot2")
library( "gplots" )
library( "RColorBrewer" )
library(tidyr)
library(clusterProfiler)
args <- commandArgs(trailingOnly = TRUE)
dirIn=paste0("/storage/chenlab/Users/junwang/human_meta/data/age_DESeq2_75_age_interval_batch/",args[1])

dir.create(dirIn,recursive = TRUE)
setwd(dirIn)
dirIn <- getwd()
all_data=NULL
file=paste0("/storage/chenlab/Users/junwang/human_meta/data/age_DESeq2_75_age_interval_batch/",args[1],"/",args[1],"_DEGs_bulk.txt")

data=read.table(file,header=T)
datalist=data$rowNameResordered
engene_entrez= bitr(data$rowNameResordered, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")

n=match(engene_entrez$SYMBOL,datalist,nomatch=0)

geneList=data[n,]$log2FoldChange

m=match(data[n,]$rowNameResordered,engene_entrez$SYMBOL,nomatch=0)

names(geneList)=engene_entrez[m,]$ENTREZID

geneList=sort(geneList, decreasing = TRUE)

#data1=data[((data$log2FoldChange>=1)|(data$log2FoldChange<=-1))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered
data1=data[(data$padj<0.05)&(!is.na(data$padj)),]$rowNameResordered

#data1=data[((data$log2FoldChange>=0.5)|(data$log2FoldChange<=-0.5))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered
all_data=c(all_data,data1)
#}

genename=unique(all_data)

#all_data_up=data[((data$log2FoldChange>=1))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered

#all_data_up=data[((data$log2FoldChange>=0.5))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered
all_data_up=data[((data$log2FoldChange>0))&(data$padj<0.05)&(!is.na(data$padj)),]$rowNameResordered
all_data_down=data[((data$log2FoldChange<0))&(data$padj<0.05)&(!is.na(data$padj)),]$rowNameResordered

#all_data_down=data[((data$log2FoldChange<=-0.5))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered
#all_data_down=data[((data$log2FoldChange<=-1))&(data$padj<0.01)&(!is.na(data$padj)),]$rowNameResordered
exp=read.table(paste0("/storage/chenlab/Users/junwang/human_meta/data/genexp_donor_cell_raw_batch_new/exp_",args[1]),header=T)

file_info=read.table("/storage/chenlab/Users/junwang/human_meta/data/atlasrna_metadata_chen.txt",header=T)

file_info1=file_info[order(file_info$age),]

fListNames=colnames(exp)
m=match(file_info1[order(file_info1$age),]$sampleid,fListNames,nomatch=0)
############
exp1=exp[,m]
#exp1=exp[,order(file_info1$V1)]

donor_name=colnames(exp1)
k=match(donor_name,file_info1$sampleid)
#colnames(exp_order)=paste0(file_info1[k,]$V2,"_",donor_name)

file_info1$age_interval = "53_65"
#file_info1[file_info1$V2>60&file_info1$V2<=65,]$age_interval="61_65"

file_info1[file_info1$age>65&file_info1$age<=70,]$age_interval="66_70"
#file_info1[file_info1$V2>70&file_info1$V2<=80,]$age_interval="71_80"
file_info1[file_info1$age>70&file_info1$age<=75,]$age_interval="71_75"
file_info1[file_info1$age>75&file_info1$age<=80,]$age_interval="76_80"
file_info1[file_info1$age>80&file_info1$age<=85,]$age_interval="81_85"
file_info1[file_info1$age>85&file_info1$age<=91,]$age_interval="86_91"



Design=data.frame(row.names=file_info1[k,]$sampleid,age=file_info1[k,]$age,gender=file_info1[k,]$gender,race=file_info1[k,]$race, age_interval=file_info1[k,]$age_interval)
#refConditionSample="53_65"
dds    <- DESeqDataSetFromMatrix(countData = exp1,colData = Design , design = ~gender+race+age_interval)
#dds    <- DESeqDataSetFromMatrix(countData = exp1,colData = Design , design = ~gender+race+age)

#keep <- rowSums(counts(dds)) >= 10
keep <- rowMeans(counts(dds)) >= 10

dds2 = dds[keep,]
dds2$age_interval <- factor(dds2$age_interval, levels=c("53_65","66_70","71_75","76_80","81_85","86_91"))

rld <- rlog( dds2 )
colnames(rld)=paste0(file_info1[k,]$age,"_",donor_name) #file_info1[k,]$age_interval
#rownames(rld)=rownames(exp_order)
exp_rld=assay(rld)






#############
exp_gene = rownames(exp_rld)
n=match(genename,exp_gene)
exp_rld1=exp_rld[n,]

library("tibble")
library("dplyr")
library("readr")
df=as.data.frame(exp_rld1)

rownames(df)=rownames(exp_rld1)

write.table(df, file=paste0("combined_",args[1],"_DEG_padj0.05"),quote=F, sep="\t")

library("ComplexHeatmap")
#library(pheatmap)
#DT1=as.matrix(t(scale(t(df1),center=T)))
DT1=as.matrix(t(scale(t(df),center=T)))

my_sample_col <- data.frame(sample =c(file_info1[k,]$age_interval))

row.names(my_sample_col) <- colnames(DT1)

#ha=HeatmapAnnotation(Age_range=my_sample_col[colnames(DT1),1],col=list(Age_range = c( "42_60"="palegreen3","61_65"="yellow", "66_70"="lightpink2","71_75"="cyan3",     "76_80"="aquamarine", "81_85"="orange", "86_91"="red")),annotation_name_side = "right",annotation_name_gp= gpar(fontsize = 15))
ha=HeatmapAnnotation(Age_range=my_sample_col[colnames(DT1),1],col=list(Age_range = c( "53_65"="palegreen3", "66_70"="lightpink2","71_75"="cyan3",     "76_80"="aquamarine", "81_85"="yellow", "86_91"="red")),annotation_name_side = "right",annotation_name_gp= gpar(fontsize = 15))


pdf(paste0("8pheatmap_DEG_",args[1],".pdf"))
#pheatmap(df1, scale="row",cluster_cols=FALSE)
#ht=Heatmap(DT1,clustering_distance_columns = "euclidean",clustering_distance_rows = "euclidean",show_row_names = FALSE ,name = "Normalized gene expression",cluster_columns = FALSE)
ht=Heatmap(DT1,row_title = args[1],  clustering_distance_rows = "euclidean", show_row_names = FALSE, name = "Normalized gene\nexpression", top_annotation = ha, cluster_columns = FALSE)
draw(ht)
dev.off()

#############
#GO analysis
###########
#library(fgsea)
library(data.table)
#library(ggplot2)
#library(reactome.db)
library('biomaRt')
#library('BSgenome.Hsapiens.UCSC.hg38')
library("org.Hs.eg.db")
#library(magrittr)
library(clusterProfiler)
library(enrichplot)
#library(meshes)
#library(DOSE)
#library(MeSH.Hsa.eg.db)

#gene_hm= bitr(genename, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")

name_convert=function(genes,database,dataset,symbol){
ensembl <- useMart("ensembl", dataset=dataset)

foo0 <- getBM(attributes=c('entrezgene_id',
                          symbol),
             filters = symbol,
             values =genes,
             mart = ensembl)
foo=data.frame(SYMBOL=foo0[[symbol]],ENTREZID=foo0$entrezgene_id)
foo1<- getBM(attributes=c('external_synonym','entrezgene_id'),
             filters = 'external_synonym',
             values = genes,
             mart = ensembl)
foo2=data.frame(SYMBOL=foo1$external_synonym,ENTREZID=foo1$entrezgene_id)

foo3 <- getBM(attributes=c('entrezgene_id',
                           'external_gene_name'),
              filters = 'external_gene_name',
              values = genes,
              mart = ensembl)

foo4=data.frame(SYMBOL=foo3$external_gene_name,ENTREZID=foo3$entrezgene_id)

foo5=bitr(genes, fromType="SYMBOL", toType="ENTREZID", OrgDb=database)
final_data=na.omit(unique(rbind(foo,foo2,foo4,foo5)))
}

set=list(all_data,all_data_up,all_data_down)
label=c("all","up","down")
for(i in 1:length(set)){
genename=set[[i]]
label1=label[i]
#eg_hm=name_convert(genes=genename,database="org.Hs.eg.db",dataset = "hsapiens_gene_ensembl",symbol="hgnc_symbol")
eg_hm=bitr(genename, fromType="SYMBOL", toType="ENTREZID", OrgDb="org.Hs.eg.db")

gene=eg_hm$ENTREZID

library(msigdbr)
#cate=c("C5","C6","C7")
cate=c("C5")
for(c in cate){
m_df <- msigdbr(species = "Homo sapiens")
head(m_df, 2) %>% as.data.frame
m_t2g <- msigdbr(species = "Homo sapiens", category = c) %>%
  dplyr::select(gs_name, entrez_gene)
em <- enricher(gene, TERM2GENE=m_t2g,minGSSize=10, qvalueCutoff =0.05)
if(dim(summary(em))[1]!=0){

write.table(data.frame(em),file=paste0(args[1],"_msigdbr_",c,"_enricher_minGSSize10","_",label1),quote=F,sep="\t")

em_new <- setReadable(em, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
write.table(data.frame(em_new),file=paste0(args[1],"_msigdbr_",c,"_enricher_minGSSize10_geneName","_",label1),quote=F,sep="\t")


pdf(paste0(args[1],"_","msigdbr_",c,"_enricher_minGSSize10_dotPlot_Cate20","_",label1,".pdf"),width=10,height=20)
print(dotplot(em, showCategory=20))
dev.off()

#pdf(paste0("msigdbr_",c,"_enricher_minGSSize10_dotPlot_Cate14.pdf"),width=15)
#print(dotplot(em, showCategory=14))
#dev.off()


x2 <- pairwise_termsim(em) 
x2_new <- setReadable(x2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
#emapplot(x2)

pdf(paste0(args[1],"_","msigdbr_",c,"_network","_",label1,".pdf"),width=15,height=15)
#print(emapplot(em_new))
print(emapplot(x2_new))

dev.off()

#pdf(paste0(args[1],"_","msigdbr_",c,"_tree.pdf"),width=20,height=10)
#print(emapplot(em_new))
#print(treeplot(x2))


}
}


exp_gene_all=name_convert(genes=exp_gene,database="org.Hs.eg.db",dataset = "hsapiens_gene_ensembl",symbol="hgnc_symbol")


library(GOSemSim)
ego <- enrichGO(gene  = gene,
        universe      = exp_gene_all$ENTREZID,
        OrgDb         = org.Hs.eg.db,
        ont           = "MF",
        pAdjustMethod = "BH",
        pvalueCutoff  = 0.05,
        qvalueCutoff  = 0.05,
        readable      = TRUE)

if(dim(summary(ego))[1]!=0){
    d <- godata('org.Hs.eg.db', ont="MF")
    ego2 <- pairwise_termsim(ego, method = "Wang", semData = d)
    #pdf(paste0(args[1],"_","GO_MF_treeplot","_",label1,".pdf"),width=20,height=15)
    #print(treeplot(ego2, showCategory = 20 ))
    #dev.off()

    pdf(paste0(args[1],"_","GO_MF_dotplot","_",label1,".pdf"),width=20,height=15)
    print(dotplot(ego, showCategory = 20 ))
    dev.off()


    write.table(data.frame(ego),file=paste0("enrichGO_MF_",args[1],"_",label1),quote=F,sep="\t")
    em_new <- setReadable(ego2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
    write.table(data.frame(em_new),file=paste0("enrichGO_MF_readable_",args[1],"_",label1),quote=F,sep="\t")
    pdf(paste0(args[1],"_","GO_MF_network","_",label1,".pdf"),width=15,height=15)
    print(emapplot(em_new, showCategory=20))
    dev.off()

}

ego <- enrichGO(gene  = gene,
        universe      = exp_gene_all$ENTREZID,
        OrgDb         = org.Hs.eg.db,
        ont           = "BP",
        pAdjustMethod = "BH",
        pvalueCutoff  = 0.05,
        qvalueCutoff  = 0.05,
        readable      = TRUE)
if(dim(summary(ego))[1]!=0){
    d <- godata('org.Hs.eg.db', ont="BP")
    ego2 <- pairwise_termsim(ego, method = "Wang", semData = d)
#    pdf(paste0(args[1],"_","GO_BP_treeplot","_",label1,".pdf"),width=20,height=15)
 #   print(treeplot(ego2, showCategory = 20))
 #   dev.off()


     pdf(paste0(args[1],"_","GO_BP_dotplot","_",label1,".pdf"),width=20,height=15)
    print(dotplot(ego, showCategory = 20))
    dev.off()
  

  write.table(data.frame(ego),file=paste0("enrichGO_BP_",args[1],"_",label1),quote=F,sep="\t")
    em_new <- setReadable(ego2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
    write.table(data.frame(em_new),file=paste0("enrichGO_BP_readable_",args[1],"_",label1),quote=F,sep="\t")
    pdf(paste0(args[1],"_","GO_BP_network","_",label1,".pdf"),width=15,height=15)
#    treeplot(ego2, showCategory = 20)
    print(emapplot(em_new, showCategory=20))
    dev.off()

}
}

cell=args[1]

library(msigdbr)
c="C5"
m_df <- msigdbr(species = "Homo sapiens")
m_t2g <- msigdbr(species = "Homo sapiens", category = c) %>%
  dplyr::select(gs_name, entrez_gene)

em2 <- GSEA(geneList, TERM2GENE = m_t2g,minGSSize=10)

if(dim(summary(em2))[1]!=0){

em2_new <- setReadable(em2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
write.table(data.frame(em2_new),file=paste0(cell,"_","msigdbr"),quote=F,sep="\t")
pdf(paste0(cell,"_","gsea_msigdbr_dotplot.pdf"),width=18, height=20)
p=dotplot(em2_new, showCategory=20, split=".sign")+ggtitle("dotplot for msigdbr")+facet_grid(.~.sign)
print(p)
dev.off()


pdf(paste0(cell,"_","gse_msigdbr_ridgeplot.pdf"),width=18, height=20)
p=ridgeplot(em2_new, showCategory=20)+ggtitle("Ridgeplot for msigdbr")+labs(x = "enrichment distribution")
print(p)
dev.off()



edo <- pairwise_termsim(em2_new)
pdf(paste0(cell,"_","gsea_msigdbr_emapplot.pdf"),width=18, height=20)
p=emapplot(edo, showCategory=20)+ggtitle("emapplot for msigdbr")

print(p)
dev.off()
}


em2 <- gseGO(geneList     = geneList,
              OrgDb        = org.Hs.eg.db,
              ont          = "BP",
              minGSSize    = 10,
	      pvalueCutoff = 0.05,
              verbose      = FALSE
              )
if(dim(summary(em2))[1]!=0){
em2_new <- setReadable(em2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
write.table(data.frame(em2_new),file=paste0(cell,"_","GO_BP"),quote=F,sep="\t")
pdf(paste0(cell,"_","gse_GO_BP_dotplot.pdf"),width=18, height=20)
p=dotplot(em2_new, showCategory=20, split=".sign")+ggtitle("dotplot for GO BP")+facet_grid(.~.sign)
print(p)
dev.off()

pdf(paste0(cell,"_","gse_GO_BP_ridgeplot.pdf"),width=18, height=20)
p=ridgeplot(em2_new, showCategory=20)+ggtitle("Ridgeplot for GO BP")+labs(x = "enrichment distribution")
print(p)
dev.off()



edo <- pairwise_termsim(em2_new)
pdf(paste0(cell,"_","gse_GO_BP_emapplot.pdf"),width=18, height=20)
p=emapplot(edo, showCategory=20)+ggtitle("emapplot for GO BP")

print(p)
dev.off()
}


em2 <- gseKEGG(geneList     = geneList,
               organism     = 'hsa',
               minGSSize    = 10,
               pvalueCutoff = 0.05,
               verbose      = FALSE)

if(dim(summary(em2))[1]!=0){
em2_new <- setReadable(em2, OrgDb ="org.Hs.eg.db", keyType="ENTREZID")
write.table(data.frame(em2_new),file=paste0(cell,"_","KEGG"),quote=F,sep="\t")
pdf(paste0(cell,"_","gse_KEGG_dotplot.pdf"),width=18, height=20)
p=dotplot(em2_new, showCategory=20, split=".sign")+ggtitle("dotplot for KEGG")+facet_grid(.~.sign)
print(p)
dev.off()

pdf(paste0(cell,"_","gse_KEGG_ridgeplot.pdf"),width=18, height=20)
p=ridgeplot(em2_new, showCategory=20)+ggtitle("Ridgeplot for KEGG")+labs(x = "enrichment distribution")
print(p)
dev.off()



edo <- pairwise_termsim(em2_new)
pdf(paste0(cell,"_","gse_KEGG_emapplot.pdf"),width=18, height=20)
p=emapplot(edo, showCategory=20)+ggtitle("emapplot for KEGG")

print(p)
dev.off()

}

