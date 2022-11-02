#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
f=/storage/singlecell/jinli/wkfl/atlashumanprj/integration/snRNA/scrnascanpyconcat2h5ad/chen82_hackney.h5ad
outdir=$(mrrdir.sh)

function cmd {
local f=$1
local bname=$(basename "$f" .h5ad)
slurmtaco.sh -t 2 -m 100G -- scrnah5adsubsetbycelltype.sh -l scpred_prediction -v BC -d "$outdir" -b "$bname" -- "$f"
}

source env_parallel.bash
env_parallel cmd ::: "$f"
