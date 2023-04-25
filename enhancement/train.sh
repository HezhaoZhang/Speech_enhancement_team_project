#!/bin/bash
#SBATCH --partition=dcs-gpu
#SBATCH --account=dcs-res
#SBATCH --cpus-per-task=10
#SBATCH --nodes=1
#SBATCH --time=20:00:00
#SBATCH --gpus-per-node=1
#SBATCH --mem=32G
#SBATCH --output=./results_hpc/output_%j.txt

module load Anaconda3/5.3.0
module load CUDAcore/11.1.1
source activate tp


python /home/acp22hz/Speech_enhancement_team_project/corpus_split/split_data.py
python train.py train_hpc.yaml --device=cuda:0