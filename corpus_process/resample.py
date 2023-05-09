import os
from torchaudio.transforms import Resample
import soundfile as sf
import torchaudio
from tqdm import tqdm


def resample_wav_files(orig_folder, new_folder, orig_sr, new_sr):
    transform = Resample(orig_sr, new_sr)
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)
    for file in tqdm(os.listdir(orig_folder), desc=f"resample {orig_folder}"):
        if file.endswith(".wav"):
            file_path = os.path.join(orig_folder, file)
            waveform, sample_rate = torchaudio.load(file_path)
            resampled_waveform = transform(waveform)
            resampled_file_path = os.path.join(new_folder, file)
            torchaudio.save(resampled_file_path, resampled_waveform, new_sr, format="wav")


if __name__ == "__main__":
    dataset_id = '0'
    print(dataset_id)
    orig_folder = f"../data/corpus/corpus-{dataset_id}"
    new_folder = f"../data/corpus/corpus-{dataset_id}-resample"
    resample_wav_files(orig_folder, new_folder, 48000, 16000)
