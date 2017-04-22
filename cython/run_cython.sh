#!/bin/bash

#SBATCH -p serial_requeue
#SBATCH -J cython_full_write
#SBATCH -n 50                 #Number of cores
#SBATCH -N 1
#SBATCH -t 10:00:00           #Runtime in minutes
#SBATCH --mem=100000                     #Memory per cpu in MB (see also --mem)
#SBATCH -o cython.o%j       #File to which standard out will be written
#SBATCH -e cython.e%j       #File to which standard err will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alw167@mail.harvard.edu

module load legacy/0.0.1-fasrc01
module load centos6/cython-0.20_python-3.3.2
module load gcc/5.2.0-fasrc02
module load python/3.4.1-fasrc01

python setup.py build_ext --inplace

python run_full_write.py
