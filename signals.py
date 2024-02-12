import numpy as np
import sounddevice as sd
import wavio as wv
import matplotlib.pyplot as plt

from scipy.fft import fft


class SignalProcessor:
    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate

        self.audio_data = None
        self.fft_data = None

    def set_default_signal(self, interval):
        self.audio_data = np.zeros(interval)

    def record_signal(self, duration: float):
        self.audio_data = sd.rec(int(duration * self.sample_rate),
                                 samplerate=self.sample_rate, channels=1)
        sd.wait()

    def update_signal(self, interval):
        duration = interval / self.sample_rate

        new_data = sd.rec(int(duration * self.sample_rate),
                          samplerate=self.sample_rate, channels=1)
        sd.wait()

        new_data.reshape(-1)

        self.audio_data = self.audio_data[interval:]
        self.audio_data = np.append(self.audio_data, new_data)

        self.fft_data = None

        return new_data

    def write_signal_to_file(self, file_name: str):
        wv.write(file_name, self.audio_data, self.sample_rate, sampwidth=2)

    def fft_signal(self, interval, output_type='dB'):
        epsilon = 1e-7
        self.fft_data = np.abs(fft(self.audio_data, interval))[0:interval // 2] + epsilon
        if output_type == 'dB':
            self.fft_data = 20 * np.log10(self.fft_data)

    def plot_signal(self, axs):
        axs.set_title("Signal")

        signal_length = self.audio_data.shape[0] / self.sample_rate
        time_list = np.linspace(0, signal_length, self.audio_data.shape[0])
        axs.plot(time_list, self.audio_data, color='k')

        axs.set_xlabel("Time")
        axs.set_ylabel("Amplitude")

    def plot_fft(self, interval, axs, plot_type='log'):
        if self.fft_data is None:
            self.fft_signal(interval)
        fft_abs = self.fft_data
        freqs = np.linspace(0, self.sample_rate // 2, interval // 2)
        axs.plot(freqs, fft_abs, color='k')

        if plot_type == 'log':
            axs.set_xscale('log')

        plt.xlabel('Frequency [Hz]')
        plt.ylabel('PSD [dB]')

    @property
    def get_audio_data(self):
        if self.audio_data is None:
            raise ValueError("Audio data is not set")
        return self.audio_data

    @property
    def get_fft_data(self):
        if self.fft_data is None:
            raise ValueError("Fourie-transform data is not set")
        return self.fft_data

    def moving_average(self, window_size):
        window = np.ones(window_size) / window_size
        self.audio_data = np.convolve(self.audio_data, window, mode='same')
