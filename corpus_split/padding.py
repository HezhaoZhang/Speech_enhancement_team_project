import soundfile as sf
import numpy as np
from scipy import fft
import multiprocessing
import os
from tqdm import tqdm


def componsate_delay(s, x):
    d = compute_delay(s, x)
    s_padded = np.pad(s, (d, 0), 'constant', constant_values=(0, 0))
    x_padded = np.pad(x, (0, d), 'constant', constant_values=(0, 0))
    return s_padded, x_padded


def compute_delay(s, x):
    length_s = len(s)
    length_x = len(x)
    padsize = length_s + length_x + 1
    padsize = 2 ** (int(np.log(padsize) / np.log(2)) + 1)
    s_pad = np.zeros(padsize)
    s_pad[:length_s] = s
    x_pad = np.zeros(padsize)
    x_pad[:length_x] = x
    corr = fft.ifft(fft.fft(s_pad) * np.conj(fft.fft(x_pad)))
    ca = np.absolute(corr)
    xmax = np.argmax(ca)
    if xmax > padsize // 2:
        return padsize - xmax
    else:
        return xmax


def pad_and_save_wav_file(args):
    file, source_folder, target_ref_folder, target_deg_folder, ref_folder = args
    file_name = os.path.splitext(file)[0]
    s_path = os.path.join(ref_folder, file)
    x2_path = os.path.join(source_folder, file)

    s, fs = sf.read(s_path)
    x2, fs = sf.read(x2_path)

    s_padded, x2_padded = componsate_delay(s, x2)

    sf.write(os.path.join(target_ref_folder, f"{file_name}.wav"), s_padded, fs)
    sf.write(os.path.join(target_deg_folder, f"{file_name}.wav"), x2_padded, fs)


def pad_wav_files(source_folder, target_ref_folder, target_deg_folder, ref_folder):
    if not os.path.exists(target_ref_folder):
        os.makedirs(target_ref_folder)
    if not os.path.exists(target_deg_folder):
        os.makedirs(target_deg_folder)

    wav_files = [file for file in os.listdir(source_folder) if file.endswith(".wav")]

    with multiprocessing.Pool() as pool:
        results = pool.imap(
            pad_and_save_wav_file,
            [(file, source_folder, target_ref_folder, target_deg_folder, ref_folder) for file in wav_files]
        )
        for _ in tqdm(results, total=len(wav_files), desc="Padding WAV files"):
            pass


if __name__ == "__main__":
    source_folder = "../data/corpus/corpus-4-0"
    target_deg_folder = "../data/corpus/corpus-4-0-padded"
    target_ref_folder = "../data/corpus/corpus-0-padded"
    ref_folder = "../data/corpus/corpus-0"
    pad_wav_files(source_folder, target_ref_folder, target_deg_folder, ref_folder)
