#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:g:rn: -l help,outdir:,bname:,groupby:,noraw,ngene: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
groupby=leiden
raw=True
ngene=100
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
		-g|--groupby)
			groupby=$2
			shift 2
			;;
		-r|--noraw)
			raw=False
			shift
			;;
		-n|--ngene)
			ngene=$2
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

[[ $bname ]] || { echo "$scriptname.sh: -b|--bname must be specified!"; exit 1; }

function cmd {
local f=$(abspath.sh "$1")
set -x
mkdir -p "$outdir" && cd "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "bname='$bname'" \
	-e "groupby='$groupby'" \
	-e "raw=$raw" \
	-e "ngene=$ngene" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
