import numpy as np
import matplotlib.pyplot as plt
import sounddevice as sd
import soundfile as sf
import pysepm
import csv
import json
import scipy.signal as sps
from do_padding import componsate_delay
from asl_P56 import asl_P56
import time
import datetime
import os
from tqdm import tqdm

#  caffeinate -u -t 80000
np.random.seed(42)
dataset_id = 2
# number of recording channels
CHANNELS = 5
# path to source data
DATA_ROOT = "../data/corpus/corpus-0"
# DATA_ROOT = "/Users/Share/corpora/VoiceBank-DEMAND/"
# path to save location
SAVE_ROOT = f"../data/corpus/corpus-{dataset_id}"
# Device ID of Aggregate Device
DEVICE_ID = 5
# Compute metrics, useful for debugging
SAVE_STATS = False
# Volume adjust
SPEECH_VOLUME = 0.1  # = 0.1
NOISE_VOLUME = 0.2


def get_stats(s, y, fs):
    playback_level = 20 * np.log10(np.max(np.abs(s)))
    input_level = 20 * np.log10(np.max(np.abs(y)))

    try:
        # resample to 16kHz such that the PESQ score can be computed
        number_of_samples = round(len(s) * float(16000) / fs)
        s_resamp = sps.resample(s, number_of_samples)
        y_resamp = sps.resample(y, number_of_samples)
        pesq_score = pysepm.pesq(s_resamp, y_resamp, 16000)[1]
        composite_score = pysepm.composite(s_resamp, y_resamp, 16000)
    except:  # if the pesq score is not available, set it to 1
        pesq_score = 1
    stoi_score = pysepm.stoi(s, y, fs)

    snrseg = pysepm.SNRseg(s, y, fgs)
    srmr = pysepm.srmr(y, fs)
    entry = {
        "playback_level": playback_level,
        "input_level": input_level,
        "pesq_score": pesq_score,
        "stoi_score": stoi_score,
        "composite_score": composite_score,
        "snrseg": snrseg,
        "srmr": srmr
    }

    print('Playback level: ', playback_level, ' dB')
    print('Input level: ', input_level, ' dB')
    print("PESQ: ", pesq_score)
    print("Composite: ", composite_score)
    print("STOI: ", stoi_score)
    print("SNRseg: ", snrseg)
    print("SRMR: ", srmr)
    return entry


def record(s_name, v_name, snr, save_stats=False):
    v = v_name
    name = s_name.split("/")[-1]  # basename of the speech file
    s, fs = sf.read(s_name)  # read the speech audio file

    # compute the active speech level
    [Px, asl, c0] = asl_P56(s, float(fs), float(16))
    # `Px` is the active speech level ms energy, asl is the active factor, and c0 is the active speech level threshold

    # Pn is the noise level ms energy (???)
    Pn = (v.conj().transpose() @ v) / len(s)

    # we scale the noise segment to obtain the desired SNR
    scale = np.sqrt(Px / Pn / (10 ** (int(snr) / 10)))
    # randomly select 7 segment of the noise file
    vs = []
    for i in range(7):
        rand_start = np.random.randint(0, v.shape[0] - s.shape[0])
        vi = v[rand_start:rand_start + s.shape[0]] * NOISE_VOLUME
        vi = vi * scale
        vs.append(vi)  # ensure the random segment is the same length as the speech
        # segment

    # print("SNR %s -> SCALE %s"%(snr,scale))
    # v = v * scale

    mix = np.column_stack([s * SPEECH_VOLUME] + vs)  # stack the noise with the signal into a stereo structure

    # play the mixture and record at the same time
    y = sd.playrec(data=mix, samplerate=fs, channels=CHANNELS, device=DEVICE_ID)
    sd.wait()

    # sf.write("wavs_train_delay/%s"%name,y,fs)

    # s,y = componsate_delay(s,y) #compensate for the delay added during recording

    # write the delay compensated reference and rerecorded wavs to file

    # sf.write("wavs_train_ref/%s"%name,s,fs)
    sf.write(f"{SAVE_ROOT}/%s" % name, y, fs)

    if save_stats == True:
        y = y[:, 0]  # get the first channel
        s, y = componsate_delay(s, y)
        entry = get_stats(s, y, fs)
    else:
        entry = {}
    # write the rerecorded audio to a file

    return entry  # return the entry to be written to the json file


if __name__ == '__main__':
    # time.sleep(60 * 60 * 1)
    start = datetime.datetime.now()
    print(start)
    out_dict = {}
    os.makedirs(SAVE_ROOT, exist_ok=True)
    # already_recorded = os.listdir(SAVE_ROOT)
    # already_recorded = [x.split(".")[0] for x in already_recorded]
    already_recorded = []
    print(DATA_ROOT)
    living, fs = sf.read(f"../data/DEMAND_48K/DLIVING/ch01.wav")
    bus, fs = sf.read(f"../data/DEMAND_48K/TBUS/ch01.wav")
    cafe, fs = sf.read(f"../data/DEMAND_48K/SCAFE/ch01.wav")
    psquare, fs = sf.read(f"../data/DEMAND_48K/SPSQUARE/ch01.wav")
    office, fs = sf.read(f"../data/DEMAND_48K/OOFFICE/ch01.wav")
    with open("log_corpus.csv") as f:
        reader = csv.reader(f)  # read the csv file
        # for each row, call record()
        next(reader, None)  # skip the header row
        for i, row in tqdm(enumerate(reader), desc=f"Recording dataset{dataset_id} with speech volume:{SPEECH_VOLUME} "
                                                   f"noise volume:{NOISE_VOLUME}", total=len(os.listdir(DATA_ROOT))):
            name, loc, snr = row
            # print(i, name, loc, snr)

            s_path = f"{DATA_ROOT}/%s" % name
            # s_file,fs = sf.read(s_path)
            if name not in already_recorded:
                if loc == "living":
                    v_path = f"{DATA_ROOT}/DEMAND_48K/DLIVING/ch01.wav"
                    v_file = living
                elif loc == "bus":
                    v_path = f"{DATA_ROOT}/DEMAND_48K/TBUS/ch01.wav"
                    v_file = bus
                elif loc == "cafe":
                    v_path = f"{DATA_ROOT}/DEMAND_48K/SCAFE/ch01.wav"
                    v_file = cafe
                elif loc == "psquare":
                    v_path = f"{DATA_ROOT}/DEMAND_48K/SPSQUARE/ch01.wav"
                    v_file = psquare
                elif loc == "office":
                    v_path = f"{DATA_ROOT}/DEMAND_48K/OOFFICE/ch01.wav"
                    v_file = office
                else:
                    print("Error: location not found")
                out_dict[name] = record(s_path, v_file, float(snr), SAVE_STATS)
                out_dict['time'] = str(datetime.datetime.now())
                # print("----------------------------------------------------")

                if i % 5 == 0:  # save the json file every 5 entries
                    with open("out_details_test.json", "w") as f:
                        json.dump(out_dict, f, indent=4)
                        count = datetime.datetime.now()
                        f.close()
                        # print(count, '\t', start)
                        # print("saved json file")
