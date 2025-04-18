import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.intro import showVideo
import numpy as np


def load_stylesheet(path):
    with open(path, "r") as f:
        return f.read()
    
def start_main():
    window = MainWindow()
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = np.random.randint(0,1000)
    if a == 11:
        intro = "assets/icons/rotoma.gif"
    else:
        intro = "assets/icons/intro.gif"
    app.setStyleSheet(load_stylesheet("assets/darkmode.qss"))
    intro = showVideo(intro, callback=start_main)
    intro.show()
    sys.exit(app.exec())