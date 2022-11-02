#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local ncell=$2
local minacc=$3
local bname=$(basename "$f" .h5ad)_n${ncell}_a${minacc}
if fileexists.sh "$f"
then
	slurmtaco.sh -t 8 -m 100G -x d01 -- sccafoptimizeovercluster.sh -e sccaf -d "$outdir" -b "$bname" -n "$ncell" -c leiden -a "$minacc" -t 8 -u hvg -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad ::: 0 ::: 0.95 0.98
