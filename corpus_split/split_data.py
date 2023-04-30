import os
import zipfile
import shutil
from sklearn.model_selection import train_test_split
# from tqdm import tqdm
import argparse

def split_wav_files(zip_file_path, output_path, train_ratio=0.7, test_ratio=0.2, random_state=None):
    output_path = os.path.join(output_path, os.path.splitext(os.path.basename(zip_file_path))[0] + "-split")
    os.makedirs(output_path, exist_ok=True)

    train_dir = os.path.join(output_path, 'train')
    test_dir = os.path.join(output_path, 'test')
    valid_dir = os.path.join(output_path, 'valid')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)
    os.makedirs(valid_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
        wav_file_names = [name for name in zip_file.namelist() if name.endswith('.wav')]

        train_files, test_valid_files = train_test_split(wav_file_names, train_size=train_ratio,
                                                         random_state=random_state)
        test_files, valid_files = train_test_split(test_valid_files, train_size=test_ratio / (1 - train_ratio),
                                                   random_state=random_state)

        def save_wav_files(files, folder):
            for file_name in files:
                with zip_file.open(file_name) as wav_file:
                    output_path = os.path.join(folder, os.path.basename(file_name))
                    with open(output_path, 'wb') as output_file:
                        shutil.copyfileobj(wav_file, output_file)

        save_wav_files(train_files, train_dir)
        save_wav_files(test_files, test_dir)
        save_wav_files(valid_files, valid_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split WAV files into train, test, and validation sets")
    parser.add_argument("input_path", help="Path to the data folder containing the zip files")
    parser.add_argument("output_path", help="Path where the split files will be saved")
    parser.add_argument("data_id", help="dataset id")
    args = parser.parse_args()

    input_path = args.input_path
    output_path = args.output_path
    data_id = args.data_id

    zip_file_path = os.path.join(input_path, 'corpus-0.zip')
    split_wav_files(zip_file_path, output_path, random_state=42)
    
    print("output_path",output_path)
    zip_file_path = os.path.join(input_path, f'corpus-{data_id}.zip')
    split_wav_files(zip_file_path, output_path, random_state=42)
    print("output_path",output_path)
    # Exract all wav files from corpus zip file and split into train/text/valid folders under data/corpus-id/
    # bessemer
    # data_folder = "/fastdata/acp22hz/"
    # output_path = '/scratch'
    # stanage
    # data_folder = "/mnt/parscratch/users/acp22hz/"
    # output_path = '/tmp/users/acp22hz/'

    # zip_file_path = data_folder+'corpus-0.zip'
    # split_wav_files(zip_file_path, output_path, random_state=42)


    # zip_file_path = data_folder+'/corpus-3_1.zip'
    # split_wav_files(zip_file_path, output_path, random_state=42)
