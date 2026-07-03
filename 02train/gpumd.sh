#!/bin/bash
#SBATCH -J dp  #作业名
#SBATCH -p hgpu8
#SBATCH --cpus-per-task=1  #cpu核心
#SBATCH --gres=gpu:1  #GPU数量


module load cuda/11.5
module load gcc/7.5.0
export PATH=/data1/home/hhu01/jieji/GPUMD/GPUMD-master/src:$PATH
nep > log
