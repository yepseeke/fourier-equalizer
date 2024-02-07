import numpy as np
import sounddevice as sd
import wavio as wv
import matplotlib.pyplot as plt

from scipy.fft import fft


def moving_average(signal, window_size):
    window = np.ones(window_size) / window_size
    smoothed_signal = np.convolve(signal, window, mode='same')

    return smoothed_signal


def record_signal(duration: float, sample_rate: int):
    recording = sd.rec(int(duration * sample_rate),
                       samplerate=sample_rate, channels=1)
    sd.wait()

    return recording


def write_signal_to_file(file_name: str, data, sample_rate: int):
    wv.write(file_name, data, sample_rate, sampwidth=2)


def signal_fft(signal, interval: int):
    epsilon = 1e-7
    transformed_signal = np.abs(fft(signal, interval))[0:interval // 2] + epsilon

    return transformed_signal


def plot_signal(signal, sample_rate: int, axs):
    axs.set_title("Signal")

    signal_length = signal.shape[0] / sample_rate
    time_list = np.linspace(0, signal_length, signal.shape[0])
    axs.plot(time_list, signal, color='k')

    axs.set_xlabel("Time")
    axs.set_ylabel("Amplitude")


def plot_fft(signal, interval: int, sample_rate: int, axs, plot_type='log'):
    fft_abs = 20 * np.log10(signal_fft(signal, interval))
    freqs = np.linspace(0, sample_rate // 2, interval // 2)
    axs.plot(freqs, fft_abs, color='k')

    if plot_type == 'log':
        axs.set_xscale('log')

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [dB]')
