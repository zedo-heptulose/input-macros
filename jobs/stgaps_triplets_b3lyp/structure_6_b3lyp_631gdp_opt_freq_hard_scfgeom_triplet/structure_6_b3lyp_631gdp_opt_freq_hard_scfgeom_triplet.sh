#!/bin/bash

#SBATCH --job-name=structure_6_b3lyp_631gdp_opt_freq_hard_scfgeom_triplet

#SBATCH --mail-user=gdb20@fsu.edu
#SBATCH --mail-type=END

#SBATCH -n 4
#SBATCH -N 1

#SBATCH -p genacc_q

#SBATCH -t 0-12:00:00
#SBATCH --mem=16GB

module load gnu openmpi orca

/gpfs/research/software/orca/orca_5_0_1_linux_x86-64_openmpi411/orca structure_6_b3lyp_631gdp_opt_freq_hard_scfgeom_triplet.inp > structure_6_b3lyp_631gdp_opt_freq_hard_scfgeom_triplet.out
