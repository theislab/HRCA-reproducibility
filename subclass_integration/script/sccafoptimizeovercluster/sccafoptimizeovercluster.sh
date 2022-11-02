#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o hd:b:e:n:c:s:a:u:t: -l help,outdir:,bname:,condaenv:,ncell:,clusterlabel:,seed:,minacc:,use:,numthreads:,noplot --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

outdir=.
ncell=0
clusterlabel=leiden
seed=12345
minacc=0.9
use=raw
numthreads=4
plot=True
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
		-e|--condaenv)
			condaenv=$2
			shift 2
			;;
		-n|--ncell)
			ncell=$2
			shift 2
			;;
		-c|--clusterlabel)
			clusterlabel=$2
			shift 2
			;;
		-s|--seed)
			seed=$2
			shift 2
			;;
		-a|--minacc)
			minacc=$2
			shift 2
			;;
		-u|--use)
			use=$2
			shift 2
			;;
		-t|--numthreads)
			numthreads=$2
			shift 2
			;;
		--noplot)
			plot=False
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
if [[ $condaenv ]]
then
	source "$(conda info --base)/etc/profile.d/conda.sh"
	conda activate "$condaenv"
fi

local f=$(abspath.sh "$1")
set -xe
hdf5ls.sh "$f"
mkdir -p "$outdir" && cd "$outdir" && pycmd.sh \
	-e "f='$f'" \
	-e "bname='$bname'" \
	-e "ncell=$ncell" \
	-e "clusterlabel='$clusterlabel'" \
	-e "seed=$seed" \
	-e "minacc=$minacc" \
	-e "use='$use'" \
	-e "numthreads=$numthreads" \
	-e "plot=$plot" \
	-s "$absdir/python/$scriptname.py"
}

if (($#))
then
	cmd "$@"
fi
