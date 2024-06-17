#!/bin/bash

#SBATCH --job-name=diradical_alkyne_b3lyp_631gdp_opt_freq_normal_triplet

#SBATCH --mail-user=gdb20@fsu.edu
#SBATCH --mail-type=END

#SBATCH -n 16
#SBATCH -N 1

#SBATCH -p genacc_q

#SBATCH -t 2-00:00:00
#SBATCH --mem=64GB

module load gnu openmpi orca

/gpfs/research/software/orca/orca_5_0_1_linux_x86-64_openmpi411/orca diradical_alkyne_b3lyp_631gdp_opt_freq_normal_triplet.inp > diradical_alkyne_b3lyp_631gdp_opt_freq_normal_triplet.out
