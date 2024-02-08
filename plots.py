import numpy as np
import pyqtgraph as pg

from PyQt5 import QtCore, QtWidgets
from scipy import signal
from signals import *


class SignalPlot(QtWidgets.QMainWindow):
    def __init__(self, window_size: int, sample_rate: int, interval: int):
        super().__init__()

        self.window_size = window_size
        self.sample_rate = sample_rate
        self.interval = interval

        self.time = np.linspace(0, self.window_size, window_size * self.sample_rate)
        self.values = np.zeros(self.window_size * self.sample_rate)

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
        duration = self.interval / self.sample_rate

        get_signal = record_signal(duration, self.sample_rate)

        self.values = self.values[self.interval:]
        self.values = np.append(self.values, get_signal.reshape(-1))

        self.line.setData(self.time, self.values)


class FFTPlot(QtWidgets.QMainWindow):
    def __init__(self, sample_rate: int, interval: int, plot_type='log'):
        super().__init__()

        self.sample_rate = sample_rate
        self.interval = interval

        # Creating array of frequencies
        self.freqs = np.linspace(0, sample_rate // 2, interval // 2)

        # Defining values of the amplitude spectrum
        duration = self.interval / self.sample_rate
        self.signal = record_signal(duration, self.sample_rate).reshape(-1)
        transformed_signal = signal_fft(self.signal, self.interval)
        self.values = 20 * np.log(transformed_signal)

        # Creating widget
        self.plot_graph = pg.PlotWidget()

        # Widget params
        pen = pg.mkPen(color=(1, 1, 1))

        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("yellow")
        self.plot_graph.setYRange(-180, 40)
        styles = {"color": "black", "font-size": "15px"}
        self.plot_graph.setLabel("left", "PSD [dB]", **styles)
        self.plot_graph.setLabel("bottom", "Frequency [Hz]", **styles)

        if plot_type == 'log':
            self.plot_graph.setLogMode(x=True)

        # Plot data
        self.line = self.plot_graph.plot(self.freqs, self.values, pen=pen)

        # Updating plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        self.plot_graph.setYRange(-180, 40)

        # Recording new data
        new_interval = self.interval // 4
        duration = new_interval / self.sample_rate
        get_new_signal = record_signal(duration, self.sample_rate).reshape(-1)
        self.signal = self.signal[new_interval:]
        self.signal = np.append(self.signal, get_new_signal)
        transformed_signal = signal_fft(self.signal, self.interval)

        # Updating spectrum values
        self.values = []
        self.values = np.append(self.values, 20 * np.log(transformed_signal))

        self.line.setData(self.freqs, self.values)

        # Applying filter
        # sos = signal.ellip(3, 5, 40, 300, 'hp', fs=self.sample_rate, output='sos')
        # filtered_signal = signal.sosfilt(sos, get_signal)
        #
        # transformed_signal = signal_fft(filtered_signal, self.interval)
        #
        # self.values = 20 * np.log(transformed_signal)
        # self.line.setData(self.freqs, self.values)
