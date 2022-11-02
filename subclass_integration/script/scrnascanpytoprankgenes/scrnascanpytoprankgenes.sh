#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:g:n: -l help,outdir:,bname:,group:,ntop: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
ntop=20
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
		-g|--group)
			group+=("$2")
			shift 2
			;;
		-n|--ntop)
			ntop=$2
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
f='$f'
bname='$bname'
ntop=$ntop
groups=$(basharr2pylist.sh -c -- "${group[@]}")
exec(open('$absdir/python/$scriptname.py').read())
"
}

if (($#))
then
	cmd "$@"
fi
