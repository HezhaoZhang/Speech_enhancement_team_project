import os
import soundfile as sf
import multiprocessing as mp


def read_wav_files(folder_name):
    _wav_files = [file for file in os.listdir(folder_name) if file.endswith('.wav')]
    return _wav_files


def split_channels_task(wav_file, _input_folder, selected_channel):
    audio, samplerate = sf.read(os.path.join(_input_folder, wav_file))

    output_folder_name = f'{_input_folder}-{selected_channel}'
    if not os.path.exists(output_folder_name):
        os.makedirs(output_folder_name)

    output_wav = audio[:, selected_channel]
    sf.write(os.path.join(output_folder_name, wav_file), output_wav, samplerate)


def split_channels(input_wav_files, _input_folder, selected_channel):
    with mp.Pool(8) as pool:
        tasks = [(wav_file, _input_folder, selected_channel) for wav_file in
                 input_wav_files]
        pool.starmap(split_channels_task, tasks, chunksize=100)


if __name__ == "__main__":
    input_folder = "../data/corpus/corpus-4"
    selected_channel = 1  # Select the channel you want to output (0-indexed)

    wav_files = read_wav_files(input_folder)
    split_channels(wav_files, input_folder, selected_channel)

