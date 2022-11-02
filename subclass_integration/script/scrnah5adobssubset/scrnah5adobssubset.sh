#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:s:n -l help,outdir:,bname:,obs:,invert --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
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
((${#obs[@]})) || { echo "$scriptname.sh: -s|--obs must be specified!"; exit 1; }

function cmd {
local f=$1
set -xe
hdf5ls.sh "$f"
mkdir -p "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "outdir='$outdir'" \
	-e "bname='$bname'" \
	-e "obss=$(basharr2pylist.sh -c -- "${obs[@]}")" \
	-e "invert=$invert" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
