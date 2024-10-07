#!/bin/bash

#SBATCH --job-name=h2o2_pbepbe_6-31++Gdp
#SBATCH -n 4
#SBATCH -N 1
#SBATCH -p genacc_q
#SBATCH -t 0-00:05:00
#SBATCH --mem-per-cpu=4GB

module purge
module load gaussian16
g16 < h2o2_pbepbe_6-31++Gdp.gjf > h2o2_pbepbe_6-31++Gdp.log
