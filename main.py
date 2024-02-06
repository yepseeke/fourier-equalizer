import numpy as np
import sounddevice as sd
import wavio as wv
import pyqtgraph as pg
import matplotlib.pyplot as plt

from scipy.fft import fft
from PyQt5 import QtCore, QtWidgets
from scipy.signal import cheby1
from scipy.io.wavfile import write

sample_rate = 44100

duration = 0.1


class SignalPlot(QtWidgets.QMainWindow):
    def __init__(self, time, values):
        super().__init__()

        self.time = time
        self.values = values

        self.plot_graph = pg.PlotWidget()

        pen = pg.mkPen(color=(0, 0, 0))

        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")

        styles = {"color": "black", "font-size": "15px"}
        self.plot_graph.setLabel("left", "Amplitude", **styles)
        self.plot_graph.setLabel("bottom", "Time (min)", **styles)

        self.line = self.plot_graph.plot(self.time, self.values, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        get_signal = record_signal(duration, sample_rate)
        self.values = moving_average(get_signal.reshape(-1), 20)
        self.line.setData(self.time, self.values)


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
    # print(time_list.shape, signal.shape) # (8820,) (8820, 1)
    axs.plot(time_list, signal, color='k')

    axs.set_xlabel("Time")
    axs.set_ylabel("Amplitude")


def plot_fft(signal, interval: int, sample_rate: int, axs, plot_type='log'):
    fft_abs = 10 * np.log10(signal_fft(signal, interval))
    freqs = np.linspace(0, sample_rate // 2, interval // 2)
    axs.plot(freqs, fft_abs, color='k')

    if plot_type == 'log':
        axs.set_xscale('log')

    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [dB]')


if __name__ == '__main__':
    signal = record_signal(duration, sample_rate).reshape(-1)
    signal_length = signal.shape[0] / sample_rate
    time_list = np.linspace(0, signal_length, signal.shape[0])

    app = QtWidgets.QApplication([])
    main = SignalPlot(time_list, signal)

    main.show()
    app.exec()
