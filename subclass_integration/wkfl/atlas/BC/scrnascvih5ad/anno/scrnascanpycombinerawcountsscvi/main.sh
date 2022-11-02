#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
scvi=/storage/singlecell/jinli/wkfl/atlashumanprj/integration/snRNA/atlas/BC/scrnascvih5ad/chen82_hackney.h5ad
rawfile=/storage/singlecell/jinli/wkfl/atlashumanprj/integration/snRNA/atlas/BC/scrnah5adsubsetbycelltype/chen82_hackney.h5ad
bname=$(basename "$rawfile" .h5ad)
outdir=$(mrrdir.sh)
slurmtaco.sh -m 100G -- scrnascanpycombinerawcountsscvi.sh -d "$outdir" -b "$bname" -r "$rawfile" -v "$scvi"
