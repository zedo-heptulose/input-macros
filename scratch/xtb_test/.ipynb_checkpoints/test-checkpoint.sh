#!/bin/bash

#SBATCH --job-name=test
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -p genacc_q
#SBATCH -t 5-00:00:00
#SBATCH --mem-per-cpu=4GB

ulimit -s unlimited
export OMP_MAX_ACTIVE_LEVELS=1xtb test.xyz > test.out -P 1 --gfn2 --opt
