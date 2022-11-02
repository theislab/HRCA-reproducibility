#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
indir=$(mrrdir.sh)/barcoderename
newfile=$indir/new.txt.gz
oldfile=$indir/old.txt.gz
outdir=$(mrrdir.sh)

head.sh "$newfile" "$oldfile"

if fileexists.sh "$newfile" "$oldfile"
then
	innerjoin2.sh -S <(zcat "$newfile" | hcut.sh barcode leiden | tail -n +2) <(zcat "$oldfile" | hcut.sh barcode celltype | tail -n +2) | tofile.sh -o "$outdir/join.txt.gz"
	zcat "$outdir"/join.txt.gz | cut -f 2- | rstatarivi.sh | tofile.sh -o "$outdir/contingency.txt.gz"
fi
