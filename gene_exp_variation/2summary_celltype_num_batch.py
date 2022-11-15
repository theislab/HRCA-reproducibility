import sys
import scvelo as scv
import anndata
import pandas as pd
import os
import numpy as np

#datafile="/storage/singlecell/jinli/wkfl/metaanalysis/deg/filename/fnameinfo_145.txt"
datafile="/storage/chenlab/Users/junwang/human_meta/data/atlasrna_metadata_chen.txt"
#batch   donor   file
#Chen_a_10x3_Lobe_19_D003_NeuN   Chen_19_D003    /storage/singlecell/jinli/wkfl/metaanalysis/prvdata/lobe/scrnaseurath5ad2h5seurat/10x3_Lobe_19_D003_NeuN.h5ad
donor="/storage/chenlab/Users/junwang/human_meta/data/donor75_new1"

#dir1="/storage/chenlab/Users/junwang/human_meta/data/genexp_donor"
#os.mkdir(dir1)


def read_h5ad_list(file_list,donor):
	adata_list=[]
	with open (file_list,"r") as fl:
		for line in fl:
			info=line.strip().split()
			if(info[0] == donor):

#			if(info[1] == donor):
				adata=scv.read(info[-1])

#				adata=scv.read(info[2])
#				adata.var_names=adata.var.features
#				adata.layers["raw"] = adata.raw.X
				adata_list.append(adata)
	adata_full=anndata.concat(adata_list,join="inner") 
	return adata_full

celltype=["AC","BC","Cone","HC","MG","RGC","Rod","Astrocyte","Microglia","RPE"]
cellnum={}

#list1="/storage/chenlab/Users/junwang/human_meta/data/donor_all_reform_batch_new"
list1="/storage/chenlab/Users/junwang/human_meta/data/donor_all_reform_batch_new_all"

#list1="/storage/chenlab/Users/junwang/human_meta/data/donor_all_reform_batch"
out=open(list1,"w")
with open(donor, "r") as da:
	for line in da:
		da1=line.strip()
		data = read_h5ad_list(datafile,da1)
		for cell in celltype:
			if cell in data.obs.scpred_prediction.value_counts():
				if da1 not in cellnum:
					cellnum[da1]={}
				cellnum[da1][cell] = data.obs.scpred_prediction.value_counts()[cell]
				num_tmp=data.obs.scpred_prediction.value_counts()[cell]
				out.write(f'{da1}\t{cell}\t{num_tmp}\n')		
			else:
				if da1 not in cellnum:
					cellnum[da1]={}
				cellnum[da1][cell] = 0
				num_tmp=0
				out.write(f'{da1}\t{cell}\t{num_tmp}\n')

out.close()
df=pd.DataFrame.from_dict(cellnum)

#list="/storage/chenlab/Users/junwang/human_meta/data/donor_all_batch"
#list="/storage/chenlab/Users/junwang/human_meta/data/donor_all_batch_new"
list="/storage/chenlab/Users/junwang/human_meta/data/donor_all_batch_new_all"

df.to_csv(f'{list}_celltype_num')
	
