#!/bin/bash
#SBATCH --time=8:00:00
#SBATCH --output=./results_hpc/output_%j.txt
#SBATCH --partition=gpu
#SBATCH --qos=gpu
#SBATCH --gres=gpu:1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=64G

module load Anaconda3/2022.10
# module load cuDNN/8.4.1.50-CUDA-11.7.0
module load CUDA/11.7.0
source activate tp

mkdir -m 700 -p /tmp/users/$USER

python ../corpus_split/split_data.py /mnt/parscratch/users/acp22hz/ /tmp/users/acp22hz/ 3_1
python train.py train_hpc.yaml --device=cuda:0

rm -rf /tmp/users/$USER