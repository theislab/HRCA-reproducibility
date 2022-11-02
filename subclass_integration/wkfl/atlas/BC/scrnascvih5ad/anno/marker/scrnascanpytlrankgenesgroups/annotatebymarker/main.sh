#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
rankdir=$(mrrdir.sh ../scrnascanpytoprankgenes)
outfile=$(mrrdir.sh)/anno.txt.gz

function cmd {
local f=$1
local group=$(basename "$f" _n20.txt.gz | sed "s/chen82_hackney_rankgene_g//")
# leftjoin2.sh -S -1 1 -2 2 <(zcat "$f" | tail -n +2) <(merscopegenes.sh --hstab | cutf.sh -f 2,1) | sort.sh -k 5,5gr | pendlines.sh -p "$group\t"
leftjoin2.sh -S -1 1 -2 2 <(zcat "$f" | tail -n +2) <(merscopegenes.sh --hs) | sort.sh -k 5,5gr | pendlines.sh -p "$group\t"
echo
}

source env_parallel.bash
(
	strjoin.sh cluster topgene logfoldchanges pvals pvals_adj scores merfish
	env_parallel -k cmd ::: "$rankdir"/*.gz
) | tofile.sh -o "$outfile"
