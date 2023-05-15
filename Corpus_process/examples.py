import csv
import json
import os
import soundfile as sf

# %% Step 1: Read the CSV file and random select filenames for each distinct (noisetype, snr) tuple.
csv_file = '../Recorder/log_corpus.csv'
with open("../Enhancement_lstm/results/4234-1/test.json") as f:
    test = json.load(f)
test = list(test.keys())

unique_tuples = set()
selected_files = {}

with open(csv_file, 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        current_tuple = (row['noisetype'], row['snr'])
        if current_tuple not in unique_tuples and row['filename'].split(".")[0] in test:
            unique_tuples.add(current_tuple)
            selected_files[row['filename']] = (row['noisetype'], row['snr'])

# %% Step 2: Store the selected filenames along with their noisetype and snr values in a JSON file.
output_json = '../data/examples/selected_files.json'
with open(output_json, 'w') as jsonfile:
    json.dump(selected_files, jsonfile)

# %% Step 3 and 4: Read the WAV files using the soundfile library in Python and save them to a new folder.
# Step 3 and 4: Read the WAV files using the soundfile library in Python and save them to a new folder.
corpus_ids = [5]
channel_ids = [0,1,2]
input_folders = [f'../data/corpus/corpus-{corpus_id}-{channel_id}' for corpus_id in corpus_ids for channel_id in
                 channel_ids]
#input_folders += ['../data/corpus/corpus-1']

output_folder = '../data/examples'
# Iterate over each input folder
for input_folder in input_folders:

    # Iterate over the files in the selected_files list
    for filename in selected_files:
        # Find the corresponding input path for the current file
        input_path = os.path.join(input_folder, filename)

        # Check if the input path exists, i.e., the file is in the current input folder
        if os.path.exists(input_path):
            output_subfolder = f'{input_folder.split("/")[-1]}-examples-original'
            output_path = os.path.join(output_folder, output_subfolder, filename)

            # Create the output folder if it doesn't exist
            os.makedirs(os.path.join(output_folder, output_subfolder), exist_ok=True)

            # Read the WAV file and save it to the output folder
            data, samplerate = sf.read(input_path)
            sf.write(output_path, data, samplerate)

files = ['p334_275.wav', 'p363_217.wav', 'p307_332.wav', 'p336_199.wav', 'p343_287.wav', 'p334_249.wav', 'p302_263.wav',
         'p341_143.wav', 'p339_281.wav', 'p251_295.wav', 'p257_207.wav', 'p302_288.wav', 'p257_213.wav', 'p364_041.wav',
         'p264_340.wav', 'p281_146.wav', 'p374_294.wav', 'p281_387.wav', 'p343_085.wav', 'p336_364.wav']
