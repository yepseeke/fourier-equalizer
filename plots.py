import pyqtgraph as pg
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QMainWindow, QVBoxLayout
from scipy import signal
from signals import SignalProcessor


class WidgetPlot(QWidget):
    def __init__(self, sample_rate: int, background_color, styles, x_label: str, y_label: str, pen_color):
        super().__init__()

        self.sample_rate = sample_rate
        self.values = None

        # Creating widget
        self.plot_graph = pg.PlotWidget()
        layout = QVBoxLayout(self)
        layout.addWidget(self.plot_graph)

        self.pen = pg.mkPen(color=pen_color)
        self.plot_graph.setBackground(background_color)

        self.plot_graph.setLabel("left", y_label, **styles)
        self.plot_graph.setLabel("bottom", x_label, **styles)

    def update_values(self, new_data):
        self.values = new_data


class SignalPlot(WidgetPlot):
    def __init__(self, sample_rate: int, window_size: int, background_color, styles, x_label: str, y_label: str,
                 pen_color):
        super().__init__(sample_rate, background_color, styles, x_label, y_label, pen_color)

        self.window_size = window_size

        self.time = np.linspace(0, self.window_size, window_size * self.sample_rate)
        self.values = np.zeros(self.window_size * self.sample_rate)

        self.line = self.plot_graph.plot(self.time, self.values, pen=self.pen)

    def update_values(self, new_data):
        new_interval = new_data.shape[0]

        self.values = self.values[new_interval:]
        self.values = np.append(self.values, new_data)

    def update_plot(self):
        self.line.setData(self.time, self.values)


class FFTPlot(WidgetPlot):
    def __init__(self, sample_rate: int, interval: int, background_color, styles, x_label: str,
                 y_label: str, pen_color, plot_type='log'):
        super().__init__(sample_rate, background_color, styles, x_label, y_label, pen_color)

        self.sample_rate = sample_rate
        self.interval = interval

        # Creating array of frequencies
        self.freqs = np.linspace(0, sample_rate // 2, interval // 2)

        # Defining zero values for the amplitude spectrum
        self.values = np.zeros(interval // 2)

        if plot_type == 'log':
            self.plot_graph.setYRange(-180, 60)
            self.plot_graph.setLogMode(x=True)

        # Plot data
        self.line = self.plot_graph.plot(self.freqs, self.values, pen=self.pen)

    def update_plot(self):
        self.plot_graph.setYRange(-10, 20)
        self.line.setData(self.freqs, self.values)


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.sample_rate = 44100
        self.interval = 4410

        duration = self.interval / self.sample_rate

        self.sound_recorder = SignalProcessor(self.sample_rate)
        self.sound_recorder.record_signal(duration)
        self.sound_recorder.fft_signal(self.interval)

        # Defining params for signal plot
        window_size = 10
        signal_styles = {"color": "black", "font-size": "15px"}
        signal_x_label = "Time(sec)"
        signal_y_label = "Amplitude"
        signal_background = (18, 74, 168)

        # Defining params for fft plot
        fft_styles = {"color": "black", "font-size": "15px"}
        fft_x_label = "Frequency [Hz]"
        fft_y_label = "PSD [dB]"
        fft_background = (255, 161, 0)

        pen_color = (0, 0, 0)

        self.fft_widget = FFTPlot(self.sample_rate, self.interval, fft_background, fft_styles, fft_x_label, fft_y_label,
                                  pen_color, plot_type='log')
        self.signal_widget = SignalPlot(self.sample_rate, window_size, signal_background, signal_styles,
                                        signal_x_label, signal_y_label, pen_color)

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

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
        new_data = self.sound_recorder.update_signal(self.interval // 4)
        self.sound_recorder.fft_signal(self.interval, output_type='linear')

        # Adding signal values to display
        self.signal_widget.update_values(new_data)

        # Adding spectrum values
        self.fft_widget.update_values(self.sound_recorder.fft_data)

    def update_plot(self):
        self.update_data()
        self.signal_widget.update_plot()
        self.fft_widget.update_plot()


def highpass(data: np.ndarray, cutoff: float, sample_rate: float, poles: int = 5):
    sos = signal.butter(poles, cutoff, 'highpass', fs=sample_rate, output='sos')
    filtered_data = signal.sosfiltfilt(sos, data)
    return filtered_data
