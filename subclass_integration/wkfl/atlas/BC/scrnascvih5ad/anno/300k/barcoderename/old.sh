#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

source trapdebug
f=/storage/singlecell/jinli/wkfl/metaanalysis/integration/add_pubdata/subcluster/Qingnan300K/BC/metadata/BC_metadata.txt.gz
outdir=$(mrrdir.sh)
zcat "$f" | awk.sh -e 'BEGIN {
getline
print "barcode", "sampleid", "donor", "celltype"
}
{
	celltype=$2
	sampleid=$3
	donor=$4
	n=split($1, arr, "-")
	print arr[1]"_"sampleid, sampleid, donor, celltype
}' | tofile.sh -o "$outdir/old.txt.gz"
