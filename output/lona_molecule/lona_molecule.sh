#!/bin/bash

#SBATCH --job-name=lona_molecule
#SBATCH -n 1
#SBATCH -N 1
#SBATCH -p genacc_q
#SBATCH -t 0-00:20:00
#SBATCH --mem-per-cpu=4GB

ulimit -s unlimited
export OMP_MAX_ACTIVE_LEVELS=1
export OMP_STACKSIZE=4G
export OMP_NUM_THREADS=4,1
/gpfs/home/gdb20/.conda/envs/crest3/bin/xtb lona_molecule.xyz > lona_molecule.out -P 1 --gfn2 --opt
