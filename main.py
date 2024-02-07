from plots import *

if __name__ == '__main__':
    sample_rate = 44100
    interval = 2205

    app = QtWidgets.QApplication([])
    # main = FFTPlot(interval=interval, sample_rate=sample_rate)
    main = SignalPlot(window_size=10, interval=interval, sample_rate=sample_rate)

    main.show()
    app.exec()
