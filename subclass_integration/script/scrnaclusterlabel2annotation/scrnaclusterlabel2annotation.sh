#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:s:c: -l help,outdir:,bname:,skip_cols:,count: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
skip_cols=1
count=50
while true
do
	case "$1" in
		-h|--help)
			exec cat "$absdir/$scriptname.txt"
			;;
		-d|--outdir)
			outdir=$2
			shift 2
			;;
		-b|--bname)
			bname=$2
			shift 2
			;;
		-s|--skip_cols)
			skip_cols=$2
			shift 2
			;;
		-c|--count)
			count=$2
			shift 2
			;;
		--)
			shift
			break
			;;
		*)
			echo "$0: not implemented option: $1" >&2
			exit 1
			;;
	esac
done

function cmd {
local f=$1
set -x
mkdir -p "$outdir" && exec Rvanilla.sh \
	-e "infile='$f'" \
	-e "outdir='$outdir'" \
	-e "bname='$bname'" \
	-e "skip_cols=$skip_cols" \
	-e "count=$count" \
	-e "source('$absdir/R/$scriptname.R')"
}

if (($#))
then
	cmd "$@"
fi
