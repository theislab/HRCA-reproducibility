#!/bin/bash

#SBATCH -o "slurm/interactive_%j.out"
#SBATCH -e "slurm/interactive_%j.err"
#SBATCH -J save_embeddings
#SBATCH -p cpu_p
#SBATCH -c 2
#SBATCH --mem=85GB
#SBATCH -t 24:00:00
#SBATCH --nice=10000

source /home/icb/ignacio.ibarra/.condainit
cmd=`head -n $SLURM_ARRAY_TASK_ID queries_postintegration_save_embeddings.sh | tail -n 1`
echo $cmd
$cmd


