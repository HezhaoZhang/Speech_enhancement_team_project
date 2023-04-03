import os
import zipfile
import shutil
from sklearn.model_selection import train_test_split
from tqdm import tqdm


def split_wav_files(zip_file_path, train_ratio=0.7, test_ratio=0.2, random_state=None):
    base_name = os.path.join("../data", os.path.splitext(os.path.basename(zip_file_path))[0] + "-split")

    os.makedirs(base_name, exist_ok=True)

    train_dir = os.path.join(base_name, 'train')
    test_dir = os.path.join(base_name, 'test')
    valid_dir = os.path.join(base_name, 'valid')
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
            for file_name in tqdm(files, desc=f"move to {folder}"):
                with zip_file.open(file_name) as wav_file:
                    output_path = os.path.join(folder, os.path.basename(file_name))
                    with open(output_path, 'wb') as output_file:
                        shutil.copyfileobj(wav_file, output_file)

        save_wav_files(train_files, train_dir)
        save_wav_files(test_files, test_dir)
        save_wav_files(valid_files, valid_dir)


# Exract all wav files from corpus zip file and split into train/text/valid folders under data/corpus-id/
zip_file_path = '../data/corpus/corpus-3_3.zip'
split_wav_files(zip_file_path, random_state=42)
