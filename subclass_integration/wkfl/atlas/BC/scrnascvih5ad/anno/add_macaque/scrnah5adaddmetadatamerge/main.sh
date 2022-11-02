#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ../../scrnascanpycombinerawcountsscvi/scrnah5adobssubset)
metadata=table.txt
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)

if fileexists.sh "$f"
then
	slurmtaco.sh -m 20G -n r03 -- scrnah5adaddmetadatamerge.sh -d "$outdir" -b "$bname" -m "$metadata" -k leiden -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
