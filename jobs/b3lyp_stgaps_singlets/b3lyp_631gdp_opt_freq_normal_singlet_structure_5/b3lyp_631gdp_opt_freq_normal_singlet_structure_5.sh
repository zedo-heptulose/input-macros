#!/bin/bash

#SBATCH --job-name=b3lyp_631gdp_opt_freq_normal_singlet_structure_5

#SBATCH --mail-user=gdb20@fsu.edu
#SBATCH --mail-type=END

#SBATCH -n 2
#SBATCH -N 1

#SBATCH -p genacc_q

#SBATCH -t 0-12:00:00
#SBATCH --mem=8GB

module load gnu openmpi orca

/gpfs/research/software/orca/orca_5_0_1_linux_x86-64_openmpi411/orca b3lyp_631gdp_opt_freq_normal_singlet_structure_5.inp > b3lyp_631gdp_opt_freq_normal_singlet_structure_5.out
