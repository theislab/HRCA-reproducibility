#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ../../scrnascanpycombinerawcountsscvi/scrnah5adobssubset)
marker=$(retinamarkermajortype.sh --hs --BC -p)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)

if fileexists.sh "$f" "$marker"
then
	slurmtaco.sh -t 2 -m 40G -x d01 -- "$(cat <<-EOF
	cat.sh "$marker"
	scrnascanpyplstackedviolin.sh --save -W 8 -H 8 -g leiden -n -d "$outdir" -b "$bname" -e -m "$marker" -- "$f"
	EOF
)"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*.h5ad
