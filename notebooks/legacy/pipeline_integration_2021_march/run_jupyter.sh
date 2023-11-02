#!/bin/bash

source ~/.profile

while getopts ":e:" opt; do
  case $opt in
    e) env="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

source ~/.condainit
printf $env
conda activate $env
jupyter lab --no-browser --ip=0.0.0.0

