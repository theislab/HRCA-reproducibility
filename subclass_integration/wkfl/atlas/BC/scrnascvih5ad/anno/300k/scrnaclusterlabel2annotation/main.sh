#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh ..)
outdir=$(mrrdir.sh)

function cmd {
local f=$1

if fileexists.sh "$f"
then
	scrnaclusterlabel2annotation.sh -d "$outdir" -b BC_label -- <(zcat "$f" | head -n -2)
fi
}

source env_parallel.bash
env_parallel cmd ::: "$indir"/contingency.txt.gz
