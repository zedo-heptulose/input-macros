#!/bin/bash

#SBATCH --job-name=oh_radical_m06-2x_6-311++Gdp
#SBATCH -n 12
#SBATCH -N 1
#SBATCH -p genacc_q
#SBATCH -t 3-00:00:00
#SBATCH --mem-per-cpu=4GB

module purge
module load gaussian16
g16 < oh_radical_m06-2x_6-311++Gdp.gjf > oh_radical_m06-2x_6-311++Gdp.log
