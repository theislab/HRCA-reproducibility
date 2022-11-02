#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ../scrnascanpyconcat2h5ad)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)
local n=$2
local key=$3
if fileexists.sh "$f"
then
	slurmtaco.sh -t 1 -m 200G --g01 -- scrnascvih5ad.sh -p 20 -n "$n" -f seurat -e scvi -d "$outdir" -b "$bname" -k "$key" -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad ::: 10000 ::: sampleid
