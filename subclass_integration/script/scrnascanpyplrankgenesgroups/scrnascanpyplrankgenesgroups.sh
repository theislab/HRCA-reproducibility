#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:H:W:g:n: -l help,outdir:,bname:,height:,width:,group:,ngene: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
height=4
width=6
ngene=20
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
		-g|--group)
			group+=("$2")
			shift 2
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
mkdir -p "$outdir" && cd "$outdir" && python3 -c "
infile='$f'
bname='$bname'
height=$height
width=$width
ngene=$ngene
groups=$(basharr2pylist.sh -c -- "${group[@]}")
exec(open('$absdir/python/$scriptname.py').read())
"
}

if (($#))
then
	cmd "$@"
fi
