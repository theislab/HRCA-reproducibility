#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
f=$(mrrdir.sh ../../scrnascanpycombinerawcountsscvi/scrnah5adobssubset)/chen82_hackney_obs.txt.gz
outdir=$(mrrdir.sh)
innerjoin2.sh -S <(zcat "$f" | hcut.sh sampleid barcode leiden | tail -n +2) ../sampleid/new2old.txt | awk.sh -e 'BEGIN {
print "barcode", "sampleid", "leiden"
}
{
	newid=$1
	barcode=$2
	leiden=$3
	sampleid=$4
	regex=newid"_"
	sub(regex, "", barcode)
	n=split(barcode, arr, "-")
	print arr[1]"_"sampleid, sampleid, leiden
}' | tofile.sh -o "$outdir/new.txt.gz"
