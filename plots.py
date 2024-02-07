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

        self.freqs = np.linspace(0, sample_rate // 2, interval // 2)
        self.values = np.zeros(interval // 2)
        self.interval = interval

        self.plot_graph = pg.PlotWidget()

        pen = pg.mkPen(color=(1, 1, 1))

        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("yellow")

        if plot_type == 'log':
            self.plot_graph.setLogMode(x=True)

        self.plot_graph.setYRange(-180, 40)

        styles = {"color": "black", "font-size": "15px"}
        self.plot_graph.setLabel("left", "PSD [dB]", **styles)
        self.plot_graph.setLabel("bottom", "Frequency [Hz]", **styles)

        self.line = self.plot_graph.plot(self.freqs, self.values, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # epsilon = 1e-7

        duration = self.interval / self.sample_rate
        get_signal = record_signal(duration, self.sample_rate).reshape(-1)

        # Applying filter
        sos = signal.ellip(3, 5, 40, 100, 'hp', fs=self.sample_rate, output='sos')
        filtered_signal = signal.sosfilt(sos, get_signal)

        transformed_signal = signal_fft(filtered_signal, self.interval)

        # windowed_fft = transformed_signal  # * signal.windows.hann(interval // 2) + epsilon

        self.values = 20 * np.log(transformed_signal)
        self.line.setData(self.freqs, self.values)
