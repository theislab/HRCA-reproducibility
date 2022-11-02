#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
f=/storage/singlecell/jinli/wkfl/atlashumanprj/integration/snRNA/atlas/BC/scrnascvih5ad/chen82_hackney.h5ad
bname=$(basename "$f" .h5ad)
outdir=$(mrrdir.sh)
if fileexists.sh "$f"
then
	slurmtaco.sh -m 40G -- scrnascanpytlrankgenesgroups.sh -g leiden -d "$outdir" -b "$bname" -- "$f"
fi
