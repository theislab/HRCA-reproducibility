#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ../../scrnascanpycombinerawcountsscvi/scrnah5adobssubset)
outdir=$(mrrdir.sh)
key=(
nCount_RNA
nFeature_RNA
pANN
percent.mt
)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)

if fileexists.sh "$f"
then
	slurmtaco.sh -t 2 -m 40G -- scrnascanpyplviolin.sh $(basharr2cmdopts.sh -o -k -- "${key[@]}") -H 5 -W 10 -n -g leiden -d "$outdir" -b "$bname" -a 90 -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
