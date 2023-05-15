import os
import wave


def get_wav_duration(file_path):
    with wave.open(file_path, 'rb') as wav_file:
        frames = wav_file.getnframes()
        rate = wav_file.getframerate()
        duration = frames / float(rate)
        return duration


def total_wav_duration(folder_path):
    total_duration = 0

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.wav'):
            file_path = os.path.join(folder_path, file_name)
            total_duration += get_wav_duration(file_path)

    return total_duration


folder_path = "../data/corpus/corpus-0"  # Replace this with the path to your folder containing WAV files
total_duration_seconds = total_wav_duration(folder_path)

print(f"Total duration of all WAV files in the folder: {total_duration_seconds:.2f} seconds")
print(f"About {total_duration_seconds/3600} hours")
