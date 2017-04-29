#!/bin/bash

#SBATCH -p GPU
#SBATCH -N 1
#SBATCH -J p100
#SBATCH --gres=gpu:p100:2
#SBATCH -t 5:00:00           #Runtime in minutes
#SBATCH -o p100.o%j       #File to which standard out will be written
#SBATCH -e p100.e%j       #File to which standard err will be written
#SBATCH --mail-type=ALL
#SBATCH --mail-user=alw167@mail.harvard.edu

module load pgi
#module load gcc/6.3.0
pgcc -acc -ta=tesla,cuda8.0 -Minfo=accel full_write_par.c
#gcc -fopenacc full_write_par.c
./a.out

rm a.out
