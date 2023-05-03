import soundfile as sf
import sys
import scipy.signal as sps
import numpy as np
import matplotlib.pyplot as plt
from scipy import fft
from pysepm import stoi


def componsate_delay(s, x):
    d = compute_delay(s, x)
    print("Delay is %d frames (%ss)" % (d, d / fs))
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
    # plt.plot(ca)
    # plt.show()
    xmax = np.argmax(ca)
    if xmax > padsize // 2:
        # fname= "s"
        # print("offset in file %s is %s samples (%s seconds)"%(fname,(padsize-xmax),(padsize-xmax)/fs))
        return padsize - xmax
    else:
        # fname= "x"
        # print("offset in file %s is %s samples (%s seconds)"%(fname,xmax,xmax/fs))
        return xmax


if __name__ == "__main__":
    name = sys.argv[1]
    s_path = "../data/corpus/corpus-0/%s.wav" % name
    x_path = "../data/corpus/corpus-1/%s.wav" % name
    x2_path = "../data/corpus/corpus-4-0/%s.wav" % name
    s, fs = sf.read(s_path)
    x, fs = sf.read(x_path)
    x2, fs = sf.read(x2_path)
    print("orignal x")
    compute_delay(s, x)
    print(stoi(s, x, fs))
    print("rerecorded x")
    compute_delay(s, x2)
    print(stoi(s, x2, fs))
    plt.subplot(3, 1, 1)
    plt.plot(s)
    plt.subplot(3, 1, 2)
    plt.plot(x)
    plt.subplot(3, 1, 3)
    plt.plot(x2)
    plt.show()

    print("delay compensated:")
    s_padded, x2_padded = componsate_delay(s, x2)
    compute_delay(s_padded, x2_padded)
    print(stoi(s_padded, x2_padded, fs))
    plt.subplot(2, 1, 1)
    plt.plot(s_padded)
    plt.subplot(2, 1, 2)
    plt.plot(x2_padded)
    plt.show()

    sf.write("debug/%s_deg.wav" % name, x2_padded, fs)
    sf.write("debug/%s_ref.wav" % name, s_padded, fs)

    """
    sf.write(name+"_padded.wav",x2,fs)
    """
