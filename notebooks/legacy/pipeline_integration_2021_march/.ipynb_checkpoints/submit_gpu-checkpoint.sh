#!/bin/bash

#SBATCH -o "slurm/interactive_%j.out"
#SBATCH -e "slurm/interactive_%j.err"
#SBATCH -J run_GPU_scib
#SBATCH -q gpu
#SBATCH -p gpu_p
#SBATCH --exclude=icb-gpusrv0[1]
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=60GB
#SBATCH -t 48:00:00
#SBATCH --nice=10000

source /home/icb/ignacio.ibarra/.condainit
# conda activate mypython3
# ipython nbconvert --to script 00_6_run_GPU_methods.ipynb
conda activate scIB-python
python 00_6_run_GPU_methods.py $SLURM_ARRAY_TASK_ID


