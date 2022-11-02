#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)

if fileexists.sh "$f"
then
	slurmtaco.sh -t 2 -m 20G -n m00 -- scrnah5ad2clean.sh -v -M -d "$outdir" -b "$bname" -- "$f"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
