#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:H:W:g:rnk:a: -l help,outdir:,bname:,height:,width:,groupby:,raw,norm,key:,angle: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
height=4
width=6
groupby=leiden
raw=False
norm=False
angle=45
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
		-H|--height)
			height=$2
			shift 2
			;;
		-W|--width)
			width=$2
			shift 2
			;;
		-g|--groupby)
			groupby=$2
			shift 2
			;;
		-r|--raw)
			raw=True
			shift
			;;
		-n|--norm)
			norm=True
			shift
			;;
		-k|--key)
			key+=("$2")
			shift 2
			;;
		-a|--angle)
			angle=$2
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
hdf5ls.sh "$f"
mkdir -p "$outdir" && cd "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "bname='$bname'" \
	-e "height=$height" \
	-e "width=$width" \
	-e "groupby='$groupby'" \
	-e "raw=$raw" \
	-e "norm=$norm" \
	-e "keys=$(basharr2pylist.sh -c -- "${key[@]}")" \
	-e "angle=$angle" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
