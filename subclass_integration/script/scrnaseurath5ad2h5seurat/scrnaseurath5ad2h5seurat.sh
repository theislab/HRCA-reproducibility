#!/usr/bin/env bash
# vim: set noexpandtab tabstop=2:

args=$(getopt -o ho:a:e: -l help,outfile:,assay:,condaenv: --name "$0" -- "$@") || exit "$?"
eval set -- "$args"

absdir=$(dirname $(readlink -f "$0"))
scriptname=$(basename "$0" .sh)

assay=RNA
while true
do
	case "$1" in
		-h|--help)
			exec cat "$absdir/$scriptname.txt"
			;;
		-o|--outfile)
			outfile=$2
			shift 2
			;;
		-a|--assay)
			assay=$2
			shift 2
			;;
		-e|--condaenv)
			condaenv=$2
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

[[ $outfile ]] || { echo "$scriptname.sh: -o|--outfile must be specified!"; exit 1; }

function cmd {
if [[ $condaenv ]]
then
	source "$(conda info --base)/etc/profile.d/conda.sh"
	conda activate "$condaenv"
fi

local f=$1
set -x
mkdir -p "$(dirname "$outfile")" && exec Rvanilla.sh \
	-e "infile='$f'" \
	-e "outfile='$outfile'" \
	-e "assay='$assay'" \
	-e "source('$absdir/R/$scriptname.R')"
}

if (($#))
then
	cmd "$@"
fi
