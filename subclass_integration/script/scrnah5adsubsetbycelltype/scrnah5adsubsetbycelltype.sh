#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:l:v:rs:n -l help,outdir:,bname:,label:,value:,raw,obs:,invert --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
label=celltype
raw=False
invert=False
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
		-l|--label)
			label=$2
			shift 2
			;;
		-v|--value)
			value+=("$2")
			shift 2
			;;
		-r|--raw)
			raw=True
			shift
			;;
		-s|--obs)
			obs+=("$2")
			shift 2
			;;
		-n|--invert)
			invert=True
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
((${#value[@]})) || { echo "$scriptname.sh: -v|--value must be specified!"; exit 1; }

function cmd {
local f=$(abspath.sh "$1")
set -x
mkdir -p "$outdir" && cd "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "bname='$bname'" \
	-e "label='$label'" \
	-e "values=$(basharr2pylist.sh -c -- "${value[@]}")" \
	-e "raw=$raw" \
	-e "obss=$(basharr2pylist.sh -c -- "${obs[@]}")" \
	-e "invert=$invert" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
