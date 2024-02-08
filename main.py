from plots import *
import os, psutil

if __name__ == '__main__':
    process = psutil.Process()

    sample_rate = 44100
    interval = 4410

    # get_signal = record_signal(1, sample_rate)
    # write_signal_to_file('sound.wav', get_signal, sample_rate)

    app = QtWidgets.QApplication([])
    main = FFTPlot(interval=interval, sample_rate=sample_rate)
    # main = SignalPlot(window_size=10, interval=interval, sample_rate=sample_rate)

    main.show()
    app.exec()
    print(process.memory_info().rss / 1024 ** 2)
