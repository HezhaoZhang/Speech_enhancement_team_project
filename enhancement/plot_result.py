import re
import matplotlib.pyplot as plt
import os

dataset_id = 2
# Read the data from the text file
corpus_id = "1"
with open(f'results_hpc/corpus-{corpus_id}/train_log.txt', 'r') as f:
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
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10))
ax1.plot(epochs, train_losses, label="Train Loss")
ax1.plot(epochs, valid_losses, label="Valid Loss")
ax1.set_xlabel("Epoch")
ax1.set_ylabel("Loss")
ax1.legend()
ax1.set_title(f"Training and Validation Losses on corpus-{corpus_id}")
ax1.grid()

# Create the line plot for STOI
ax2.plot(epochs, valid_stois, label="Valid STOI", color="green")
ax2.set_xlabel("Epoch")
ax2.set_ylabel("STOI")
ax2.legend()
ax2.set_title("Validation STOI")
ax2.grid()

plt.tight_layout()
plt.savefig(f'results_hpc/corpus-{corpus_id}-result.png')
plt.show()
