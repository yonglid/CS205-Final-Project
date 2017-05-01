#!/bin/bash

#SBATCH -p gpu
#SBATCH -J hybrid
#SBATCH -n 1                 #Number of cores
#SBATCH --gres=gpu:1
#SBATCH -t 5:00:00           #Runtime in minutes
#SBATCH --mem=10000                     #Memory per cpu in MB (see also --mem)
#SBATCH -o hybrid.o%j       #File to which standard out will be written
#SBATCH -e hybrid.e%j       #File to which standard err will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alw167@mail.harvard.edu

#module load pgi/16.10-fasrc01
module load gcc/6.3.0
#pgcc -acc -ta=tesla,cuda8.0 -Minfo=accel full_write_par.c
#gcc -fopenacc full_write_par.c
mpicc -fopenacc full_write_parMPI.c
#mpicc -fast -mp -Minfo full_write_parMPI.c
./a.out

rm a.out
