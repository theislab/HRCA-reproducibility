#!/bin/bash

#SBATCH -o "slurm/interactive_%j.out"
#SBATCH -e "slurm/interactive_%j.err"
#SBATCH -J interactive
#SBATCH -p gpu_p
#SBATCH --qos=gpu
#SBATCH -c 2
#SBATCH --mem=32GB
#SBATCH -t 6:00:00
#SBATCH --nice=10000

./run_jupyter.sh -e mypython3

