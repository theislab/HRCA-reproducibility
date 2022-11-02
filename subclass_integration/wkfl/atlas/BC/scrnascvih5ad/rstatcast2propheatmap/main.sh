#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" _obs.txt.gz)
local header=$2
local oname=${bname}_${header}
if fileexists.sh "$f"
then
	slurmtaco.sh -t 2 -m 10G -x d01 -- "$(cat <<-EOF
	zcat "$f" | hcut.sh "$header" leiden | tail -n +2 | sortcount.sh | sort.sh -k 2,2n -k 1,1 | cast.sh -N 0 | rstatcast2propheatmap.sh -W 10 -H 5 -s 8 -d "$outdir" -b "$oname"
	EOF
)"
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/*_obs.txt.gz ::: sampleid donor age gender race
