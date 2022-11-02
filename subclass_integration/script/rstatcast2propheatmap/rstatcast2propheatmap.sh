#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:W:H:s:a: -l help,outdir:,bname:,width:,height:,size:,angle: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
width=8
height=4
size=5
angle=90
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
		-W|--width)
			width=$2
			shift 2
			;;
		-H|--height)
			height=$2
			shift 2
			;;
		-s|--size)
			size=$2
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

set -x
mkdir -p "$outdir" && Rvanilla.sh \
	-e "outdir='$outdir'" \
	-e "bname='$bname'" \
	-e "width=$width" \
	-e "height=$height" \
	-e "size=$size" \
	-e "angle=$angle" \
	-e "source('$absdir/R/$scriptname.R')"
