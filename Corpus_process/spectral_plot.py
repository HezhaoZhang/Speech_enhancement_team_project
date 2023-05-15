import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

# Increase font size
plt.rcParams.update({'font.size': 16})


def plot_waveform(ax, audio_data, sample_rate, title):
    ax.plot(np.arange(len(audio_data)) / sample_rate, audio_data)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude')
    # ax.set_ylim([-0.8, 0.8])
    ax.set_title(title)


def plot_spectrogram(ax, audio_data, sample_rate, title):
    img = ax.specgram(audio_data, Fs=sample_rate, NFFT=1024, noverlap=512, scale='dB', cmap='viridis', vmax=0,
                      vmin=-200)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Frequency (Hz)')
    ax.set_title(title)
    return img


wav_file_list = ["p257_026.wav", "p257_318.wav", "p257_349.wav", "p232_251.wav"]
noisy = ["2.5_bus", "7.5_office", "12.5_cafe", "17.5_psquare"]
corpus = 5
for wav_file, noisy_type in zip(wav_file_list, noisy):
    # List of WAV files to compare
    if corpus == 5:
        filenames = [f'../data/corpus/corpus-0-resample/{wav_file}', f'../data/corpus/corpus-1-resample/{wav_file}',
                     f'../data/corpus/corpus-5-0-resample/{wav_file}', f'../data/corpus/corpus-5-1-resample/{wav_file}',
                     f'../data/corpus/corpus-5-2-resample/{wav_file}']
        titles = ["corpus 0", "corpus 1", "corpus 5 channel 0", "corpus 5 channel 1", "corpus 5 channel 2"]
    elif corpus ==4:
        filenames = [f'../data/corpus/corpus-0-resample/{wav_file}', f'../data/corpus/corpus-1-resample/{wav_file}',
                     f'../data/corpus/corpus-4-0-resample/{wav_file}', f'../data/corpus/corpus-4-3-resample/{wav_file}']
        titles = ["corpus 0", "corpus 1", "corpus 4 channel 0", "corpus 4 channel 3"]
    elif corpus  ==3:
        filenames = [f'../data/corpus/corpus-0-resample/{wav_file}', f'../data/corpus/corpus-1-resample/{wav_file}',
                     f'../data/corpus/corpus-3-0-resample/{wav_file}']
        titles = ["corpus 0", "corpus 1", "corpus 3 channel 0"]

    subtitle = f'Audio_{wav_file.split(".")[0]}_{noisy_type}_corpus_{corpus}'

    # Create a figure and axes for subplots
    n_files = len(filenames)
    fig, axes = plt.subplots(n_files * 2, 1, figsize=(12, 2 * n_files * 2), sharex=True)

    # Adjust the spacing between subplots
    plt.subplots_adjust(hspace=1)

    # Create a list to store all spectrogram data
    spectrogram_data = []

    # Read and plot waveforms and spectrograms for each file
    for idx, filename in enumerate(filenames):
        audio_data, sample_rate = sf.read(filename)

        # Plot waveform
        plot_waveform(axes[2 * idx], audio_data, sample_rate, f'Waveform of {titles[idx]}')

        # Plot spectrogram
        img = plot_spectrogram(axes[2 * idx + 1], audio_data, sample_rate, f'Spectrogram of {titles[idx]}')
        # fig.colorbar(img[3], ax=axes[2 * idx + 1]).set_label('Intensity (dB)')

    # plt.tight_layout()
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    fig.colorbar(img[3], cax=cbar_ax).set_label('Intensity (dB)')
    # plt.tight_layout()
    # plt.suptitle(subtitle)
    plt.savefig(f"../Figures/{subtitle}.png")
