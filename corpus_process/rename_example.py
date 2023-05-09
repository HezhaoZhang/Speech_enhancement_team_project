import os
import json

json_file = '../data/examples/selected_files.json'
folder_name = '../data/examples/'

# Load JSON file
with open(json_file, 'r') as f:
    file_info = json.load(f)

subfolders = os.listdir(folder_name)[1:-1]
# Iterate through subfolders
for subfolder in subfolders:
    subfolder_path = os.path.join(folder_name, subfolder)
    for wav_file in os.listdir(subfolder_path):
        if wav_file.endswith('.wav'):
            file_name, _ = os.path.splitext(wav_file)
            if wav_file in file_info:
                # Get noise type and SNR from JSON file
                noise_type, snr = file_info[wav_file]

                # Create new file name
                new_file_name = f'{file_name}-{noise_type}-{snr}.wav'

                # Rename file
                os.rename(os.path.join(subfolder_path, wav_file), os.path.join(subfolder_path, new_file_name))
