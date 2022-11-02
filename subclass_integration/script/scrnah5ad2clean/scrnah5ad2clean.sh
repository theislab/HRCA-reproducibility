#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:rlk:vs:m:M -l help,outdir:,bname:,raw,layers,key:,varindex,obs:,obsm:,fullobsm --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
raw=False
layers=False
varindex=False
fullobsm=False
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
		-r|--raw)
			raw=True
			shift
			;;
		-l|--layers)
			layers=True
			shift
			;;
		-k|--key)
			key=$2
			shift 2
			;;
		-v|--varindex)
			varindex=True
			shift
			;;
		-s|--obs)
			obs+=("$2")
			shift 2
			;;
		-m|--obsm)
			obsm+=("$2")
			shift 2
			;;
		-M|--fullobsm)
			fullobsm=True
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

function cmd {
local f=$1
set -x
mkdir -p "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "outdir='$outdir'" \
	-e "bname='$bname'" \
	-e "raw=$raw" \
	-e "layers=$layers" \
	-e "key='$key'" \
	-e "varindex=$varindex" \
	-e "obss=$(basharr2pylist.sh -c -- "${obs[@]}")" \
	-e "obsms=$(basharr2pylist.sh -c -- "${obsm[@]}")" \
	-e "fullobsm=$fullobsm" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
