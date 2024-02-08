import pyqtgraph as pg

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from scipy import signal
from signals import *


class SignalPlot(QWidget):
    def __init__(self, window_size: int, sample_rate: int):
        super().__init__()

        self.window_size = window_size
        self.sample_rate = sample_rate

        self.time = np.linspace(0, self.window_size, window_size * self.sample_rate)
        self.values = np.zeros(self.window_size * self.sample_rate)

        self.plot_graph = pg.PlotWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_graph)

        pen = pg.mkPen(color=(0, 0, 0))

        self.plot_graph.setBackground("w")

        styles = {"color": "black", "font-size": "15px"}
        self.plot_graph.setLabel("left", "Amplitude", **styles)
        self.plot_graph.setLabel("bottom", "Time (min)", **styles)

        self.line = self.plot_graph.plot(self.time, self.values, pen=pen)

        # self.timer = QtCore.QTimer()
        # self.timer.timeout.connect(self.update_plot)
        # self.timer.start()

    def update_values(self, values_to_add, new_interval):
        self.values = self.values[new_interval:]
        self.values = np.append(self.values, values_to_add)

    def update_plot(self):
        self.line.setData(self.time, self.values)


class FFTPlot(QWidget):
    def __init__(self, sample_rate: int, interval: int, plot_type='log'):
        super().__init__()

        self.sample_rate = sample_rate
        self.interval = interval

        # Creating array of frequencies
        self.freqs = np.linspace(0, sample_rate // 2, interval // 2)

        # Defining values of the amplitude spectrum

        self.values = np.zeros(interval // 2)

        # Creating widget
        self.plot_graph = pg.PlotWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_graph)

        # Widget params
        pen = pg.mkPen(color=(1, 1, 1))

        # self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("yellow")
        self.plot_graph.setYRange(-180, 40)
        styles = {"color": "black", "font-size": "15px"}
        self.plot_graph.setLabel("left", "PSD [dB]", **styles)
        self.plot_graph.setLabel("bottom", "Frequency [Hz]", **styles)

        if plot_type == 'log':
            self.plot_graph.setLogMode(x=True)

        # Plot data
        self.line = self.plot_graph.plot(self.freqs, self.values, pen=pen)

    def update_values(self, new_data, interval):
        transformed_signal = signal_fft(new_data, interval)
        self.values = 20 * np.log(transformed_signal)

    def update_plot(self):
        self.plot_graph.setYRange(-180, 40)
        self.line.setData(self.freqs, self.values)

        # Applying filter
        # sos = signal.ellip(3, 5, 40, 300, 'hp', fs=self.sample_rate, output='sos')
        # filtered_signal = signal.sosfilt(sos, get_signal)
        #
        # transformed_signal = signal_fft(filtered_signal, self.interval)
        #
        # self.values = 20 * np.log(transformed_signal)
        # self.line.setData(self.freqs, self.values)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sample_rate = 44100
        self.interval = 4410
        self.audio_data = np.zeros(self.interval)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.fft_widget = FFTPlot(44100, 4410)
        self.signal_widget = SignalPlot(10, 44100)

        layout.addWidget(self.fft_widget)
        layout.addWidget(self.signal_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Updating plot
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_data(self):
        # Record new data
        new_interval = self.interval // 4
        duration = new_interval / self.sample_rate
        new_data = record_signal(duration, self.sample_rate).reshape(-1)

        # Adding signal values to display
        self.signal_widget.update_values(new_data, new_interval)

        self.audio_data = self.audio_data[new_interval:]
        self.audio_data = np.append(self.audio_data, new_data)

        # Adding spectrum values
        self.fft_widget.update_values(self.audio_data, self.interval)

    def update_plot(self):
        self.update_data()
        self.signal_widget.update_plot()
        self.fft_widget.update_plot()
