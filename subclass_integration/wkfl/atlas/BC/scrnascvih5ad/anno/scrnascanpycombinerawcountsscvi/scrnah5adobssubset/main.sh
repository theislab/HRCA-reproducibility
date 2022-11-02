#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)
obs=(
_scvi_batch
_scvi_labels
_scvi_local_l_mean
_scvi_local_l_var
)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)

if fileexists.sh "$f"
then
	slurmtaco.sh -D 626893 -t 2 -m 100G -- scrnah5adobssubset.sh -n -d "$outdir" -b "$bname" $(basharr2cmdopts.sh -o -s -- "${obs[@]}") -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
