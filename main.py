import psutil

from PyQt5.QtWidgets import QApplication
from plots import MyApp, SignalPlot, FFTPlot
from equalizer import *

if __name__ == '__main__':
    process = psutil.Process()

    # run()

    app = QApplication([])
    main = MyApp()
    main.show()

    app.exec()
    print(process.memory_info().rss / 1024 ** 2)
