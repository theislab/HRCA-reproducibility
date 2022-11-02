#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:H:W:m:g:rne -l help,outdir:,bname:,height:,width:,marker:,groupby:,raw,norm,dendrogram,meanexpr,log --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
height=4
width=6
groupby=leiden
raw=False
norm=False
dendrogram=False
meanexpr=False
log=False
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
		-m|--marker)
			marker=$2
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
		-e|--dendrogram)
			dendrogram=True
			shift
			;;
		--meanexpr)
			meanexpr=True
			shift
			;;
		--log)
			log=True
			shift
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
[[ $marker ]] || { echo "$scriptname.sh: -m|--marker must be specified!"; exit 1; }

function cmd {
local f=$(abspath.sh "$1")
local marker=$(abspath.sh "$marker")
set -x
mkdir -p "$outdir" && cd "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "marker='$marker'" \
	-e "bname='$bname'" \
	-e "height=$height" \
	-e "width=$width" \
	-e "groupby='$groupby'" \
	-e "raw=$raw" \
	-e "norm=$norm" \
	-e "dendrogram=$dendrogram" \
	-e "meanexpr=$meanexpr" \
	-e "log=$log" \
	-s "$absdir/python/$scriptname.py"

}

if (($#))
then
	cmd "$@"
fi
