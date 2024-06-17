#!/bin/bash

#SBATCH --job-name=MMM_singlet_hf_3c_of_

#SBATCH --mail-user=gdb20@fsu.edu
#SBATCH --mail-type=FAIL

#SBATCH -n 8
#SBATCH -N 1

#SBATCH -p genacc_q

#SBATCH -t 2-00:00:00
#SBATCH --mem=32GB

module load gnu openmpi orca

/gpfs/research/software/orca/orca_5_0_1_linux_x86-64_openmpi411/orca MMM_singlet_hf_3c_of_.inp > MMM_singlet_hf_3c_of_.out
