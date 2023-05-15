import re
import matplotlib.pyplot as plt
import os
import numpy as np

def read_data_from_logs(corpus_id_list):
    data = {'loss': [], 'stoi': []}

    for corpus_id in corpus_id_list:


        # Extract the numerical data using regular expressions
        if network == "lstm":
            with open(f'../data/LSTM_results_hpc/corpus-{corpus_id}/train_log.txt', 'r') as f:
                lines = f.readlines()

            # Assuming the "test loss" and "test stoi" are at the last two lines of each log file
            last_line = lines[-1]
            loss = float(re.search(r'test loss: (\d+\.?\d*e?-?\d+)', last_line).group(1))
            stoi = float(re.search(r'test stoi: (\d+\.?\d*e?-?\d+)', last_line).group(1))

            data['loss'].append(loss)
            data['stoi'].append(stoi)
        elif network == "MetricGAN":
            with open(f'../data/MetricGAN_results_hpc/corpus-{corpus_id}/train_log.txt', 'r') as f:
                lines = f.readlines()

            # Assuming the "test loss" and "test stoi" are at the last two lines of each log file
            last_line = lines[-1]
            stoi = float(re.search(r'test stoi: (\d+\.?\d*e?-?\d+)', last_line).group(1))
            data['stoi'].append(stoi)

    return data


def plot_data(data, corpus_id_list):
    if network == "lstm":
        fig, axs = plt.subplots(1, 2, figsize=(12, 6))  # Create a figure with two subplots
        corpus_id_list = [i.replace("-padded","") for i in corpus_id_list]
        # Plot Test Loss
        axs[0].bar(corpus_id_list, data['loss'], color='b')
        axs[0].set_xlabel('Corpus ID', fontsize=14)
        axs[0].set_ylabel('Test Loss', fontsize=14)
        axs[0].set_title('Test Loss across different corpora', fontsize=16)
        axs[0].tick_params(axis='both', which='major', labelsize=12)

        # Plot Test STOI
        axs[1].bar(corpus_id_list, data['stoi'], color='g')
        axs[1].set_xlabel('Corpus ID', fontsize=14)
        axs[1].set_ylabel('Test STOI', fontsize=14)
        axs[1].set_title('Test STOI across different corpora', fontsize=16)
        axs[1].tick_params(axis='both', which='major', labelsize=12)

        plt.tight_layout()
        plt.savefig('../Figures/lstm-combined-result.png')
    elif network == "MetricGAN":
        fig, axs = plt.subplots(1, 1, figsize=(12, 6))  # Create a figure with two subplots
        corpus_id_list = [i.replace("-padded", "") for i in corpus_id_list]

        # Plot Test STOI
        axs.bar(corpus_id_list, data['stoi'], color='g')
        axs.set_xlabel('Corpus ID', fontsize=14)
        axs.set_ylabel('Test STOI', fontsize=14)
        axs.set_title('Test STOI across different corpora', fontsize=16)
        axs.tick_params(axis='both', which='major', labelsize=12)

        plt.tight_layout()
        plt.savefig('../Figures/MetricGAN-combined-result.png')

# Read the data from the text file "4-3-padded",
network = "MetricGAN"
corpus_id_list = ["1-padded", "3-0-padded", "4-0-padded",  "5-0-padded", "5-2-padded"]
for corpus_id in corpus_id_list:
    if network == "lstm":
        with open(f'../data/LSTM_results_hpc/corpus-{corpus_id}/train_log.txt', 'r') as f:
            data = f.read()

        epochs, train_losses, valid_losses, valid_stois = [], [], [], []
        for line in data.strip().split("\n"):
            if line.startswith("Epoch:"):
                parts = re.findall(r"[-+]?\d*\.\d+e[+-]?\d+|\d+", line)
                epochs.append(int(parts[0]))
                train_losses.append(float(parts[1]))
                valid_losses.append(float(parts[2]))
                valid_stois.append(float(parts[3]))

        # Create the line plots for losses
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 8))
        ax1.plot(epochs, train_losses, label="Train Loss")
        ax1.plot(epochs, valid_losses, label="Valid Loss")
        ax1.set_xlabel("Epoch", fontsize=15)
        ax1.set_ylabel("Loss", fontsize=15)
        ax1.legend()
        ax1.set_title(f"Training and Validation Losses on corpus-{corpus_id}", fontsize=16)
        ax1.grid()

        # Create the line plot for STOI
        ax2.plot(epochs, valid_stois, label="Valid STOI", color="green")
        ax2.set_xlabel("Epoch", fontsize=14)
        ax2.set_ylabel("STOI", fontsize=14)
        ax2.legend()
        ax2.set_title("Validation STOI", fontsize=16)
        ax2.grid()
        plt.subplots_adjust(hspace=0.4)
        plt.savefig(f'../Figures/lstm-corpus-{corpus_id}-result.png')
    elif network == "MetricGAN":
        with open(f'../data/MetricGAN_results_hpc/corpus-{corpus_id}/train_log.txt', 'r') as f:
            data = f.read()

        epochs, train_losses, valid_sisnr, valid_pesq, valid_stois = [], [], [], [], []
        for line in data.strip().split("\n"):
            if line.startswith("Epoch:"):
                parts = re.findall(r"[-+]?\d*\.\d+e[+-]?\d+|[-+]?\d*\.\d+|\d+", line)
                epochs.append(int(parts[0]))
                train_losses.append(float(parts[1]))
                valid_sisnr.append(float(parts[2]))
                valid_pesq.append(float(parts[3]))
                valid_stois.append(float(parts[4]))

        # Create the line plots for losses
        # fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(6.4, 12))
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.4, 12))
        ax1.plot(epochs, train_losses, label="Train Loss")
        ax1.set_xlabel("Epoch", fontsize=15)
        ax1.set_ylabel("Loss", fontsize=15)
        ax1.legend()
        ax1.set_title(f"Training Losses on corpus-{corpus_id}", fontsize=16)
        ax1.grid()

        # Create the line plot for valid SI-SNR
        # ax2.plot(epochs, valid_sisnr, label="Valid SI-SNR", color="blue")
        # ax2.set_xlabel("Epoch", fontsize=14)
        # ax2.set_ylabel("SI-SNR", fontsize=14)
        # ax2.legend()
        # ax2.set_title("Validation SI-SNR", fontsize=16)
        # ax2.grid()
        #
        # # Create the line plot for valid PESQ
        # ax3.plot(epochs, valid_pesq, label="Valid PESQ", color="red")
        # ax3.set_xlabel("Epoch", fontsize=14)
        # ax3.set_ylabel("PESQ", fontsize=14)
        # ax3.legend()
        # ax3.set_title("Validation PESQ", fontsize=16)
        # ax3.grid()

        # Create the line plot for valid STOI
        ax2.plot(epochs, valid_stois, label="Valid STOI", color="green")
        ax2.set_xlabel("Epoch", fontsize=14)
        ax2.set_ylabel("STOI", fontsize=14)
        ax2.legend()
        ax2.set_title("Validation STOI", fontsize=16)
        ax2.grid()
        plt.tight_layout()
        plt.subplots_adjust(hspace=0.4)
        plt.savefig(f'../Figures/MetricGAN-corpus-{corpus_id}-result.png')

if network == "lstm":
    data = read_data_from_logs(corpus_id_list)
    plot_data(data, corpus_id_list)
elif network == "MetricGAN":
    data = read_data_from_logs(corpus_id_list)
    plot_data(data, corpus_id_list)