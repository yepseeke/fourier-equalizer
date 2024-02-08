from plots import *
import psutil
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    process = psutil.Process()

    app = QApplication([])
    main = MyApp()
    main.show()

    app.exec()
    print(process.memory_info().rss / 1024 ** 2)
