#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
outdir=$(mrrdir.sh)
bname=chen82_hackney
slurmtaco.sh -t 2 -m 80G --g01 -- scrnascanpyconcat2h5ad.sh -d "$outdir" -b "$bname" -t 10 -- fnameinfo.txt
