import sounddevice as sd
import numpy as np
import time

def test_input_channels(device, channels, duration=3, samplerate=44100):
    """
    Test input channels on a device to identify them.

    Args:
        device (int): The device ID to test.
        channels (int): The number of input channels to test.
        duration (int, optional): The duration of the recording in seconds. Default is 3 seconds.
        samplerate (int, optional): The sample rate for recording. Default is 44100 Hz.

    Returns:
        None
    """
    if channels < 1:
        print("Please provide a valid number of channels.")
        return

    def record_channel(channel):
        mapping = [0] * channels
        mapping[channel] = 1
        return sd.rec(frames=duration * samplerate, samplerate=samplerate, channels=1, device=device, mapping=mapping)

    for i in range(channels):
        print(f"Recording from channel {i + 1}... ")
        recording = record_channel(i)
        sd.wait()
        print(f"Playing back channel {i + 1}...")
        sd.play(recording, samplerate=samplerate)
        sd.wait()
        time.sleep(1)

    print("Testing completed.")

if __name__ == "__main__":
    test_device = 0  # Replace with your device ID
    num_channels = 2  # Replace with the number of input channels to test
    test_input_channels(test_device, num_channels)
