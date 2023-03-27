import os
import csv
import random

random.seed(42)


def generate_csv(folder_path, output_csv):
    noise_types = ['bus', 'cafe', 'living', 'office', 'psquare']
    snr_values = [17.5, 12.5, 7.5, 2.5]

    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['filename', 'noisetype', 'snr']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for file_name in os.listdir(folder_path):
            noise_type = random.choice(noise_types)
            snr = random.choice(snr_values)
            writer.writerow({'filename': file_name, 'noisetype': noise_type, 'snr': snr})


folder_path = "../data/corpus/corpus-0"  # Replace this with the path to your folder containing the files
output_csv = "log_corpus.csv"  # Replace this with the desired output CSV file path
generate_csv(folder_path, output_csv)
