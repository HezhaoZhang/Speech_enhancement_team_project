import os
import soundfile as sf
import multiprocessing as mp


def read_wav_files(folder_name):
    _wav_files = [file for file in os.listdir(folder_name) if file.endswith('.wav')]
    return _wav_files


def split_channels_task(wav_file, _input_folder, _channels, _output_folders):
    audio, samplerate = sf.read(os.path.join(_input_folder, wav_file))
    channels_per_folder = _channels // _output_folders
    audio_channels = [audio[:, i:i + channels_per_folder] for i in range(0, _channels, channels_per_folder)]

    for idx, output_folder in enumerate(range(_output_folders)):
        output_folder_name = f'{_input_folder}_{idx}'
        if not os.path.exists(output_folder_name):
            os.makedirs(output_folder_name)

        output_wav = audio_channels[idx]
        sf.write(os.path.join(output_folder_name, wav_file), output_wav, samplerate)


def split_channels(input_wav_files, _input_folder, _channels, _output_folders):
    with mp.Pool(12) as pool:
        tasks = [(wav_file, _input_folder, _channels, _output_folders) for wav_file in input_wav_files]
        pool.starmap(split_channels_task, tasks, chunksize=100)


if __name__ == "__main__":
    input_folder = "../data/corpus/corpus-3"
    channels = 12
    output_folders = 4

    wav_files = read_wav_files(input_folder)
    split_channels(wav_files, input_folder, channels, output_folders)
