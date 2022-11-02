#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)
slurmtaco.sh -t 2 -m 100G -- scrnah5adsubsetbycelltype.sh -l scpred_prediction -v unassigned -n -d "$outdir" -b "$bname" -- "$f"
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
