import os
import random
import shutil


def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def split_wav_files(clean_folder, noisy_folder, random_seed, train_ratio=0.8, valid_ratio=0.1):
    random.seed(random_seed)

    clean_files = [f for f in os.listdir(clean_folder) if f.endswith('.wav')]
    noisy_files = [f for f in os.listdir(noisy_folder) if f.endswith('.wav')]

    pairs = [(os.path.join(clean_folder, f), os.path.join(noisy_folder, f)) for f in clean_files if f in noisy_files]

    random.shuffle(pairs)

    num_train = int(len(pairs) * train_ratio)
    num_valid = int(len(pairs) * valid_ratio)

    train_pairs = pairs[:num_train]
    valid_pairs = pairs[num_train:num_train + num_valid]
    test_pairs = pairs[num_train + num_valid:]

    return train_pairs, valid_pairs, test_pairs


def copy_files_to_folders(pairs, clean_dest_folder, noisy_dest_folder):
    create_folder(clean_dest_folder)
    create_folder(noisy_dest_folder)

    for clean_file, noisy_file in pairs:
        shutil.copy(clean_file, clean_dest_folder)
        shutil.copy(noisy_file, noisy_dest_folder)


def main():
    clean_folder = '../data/VoiceBank-DEMAND/clean_trainset_56spk_wav'
    noisy_folder = '../data/VoiceBank-DEMAND/noisy_trainset_56spk_wav'
    random_seed = 42

    train_pairs, valid_pairs, test_pairs = split_wav_files(clean_folder, noisy_folder, random_seed)

    copy_files_to_folders(train_pairs, '../data/train/clean', '../data/train/noisy')
    copy_files_to_folders(valid_pairs, '../data/valid/clean', '../data/valid/noisy')
    copy_files_to_folders(test_pairs, '../data/test/clean', '../data/test/noisy')


if __name__ == '__main__':
    main()
