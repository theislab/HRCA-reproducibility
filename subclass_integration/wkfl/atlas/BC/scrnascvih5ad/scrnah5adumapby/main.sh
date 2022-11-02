#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

labels=(
DF.classifications
age
donor
gender
race
sampleid
scpred_prediction
leiden
nCount_RNA
nFeature_RNA
pANN
percent.mt
leiden
)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)
slurmtaco.sh -t 2 -m 100G --g01 -- scrnah5adumapby.sh -d "$outdir" -b "$bname" $(basharr2cmdopts.sh -o -l -- "${labels[@]}") -- "$f"
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
