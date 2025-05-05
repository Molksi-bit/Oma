#Disclaimer:
#When writing this code only god and I knew what I was doing.
#Now only god knows. So please dont waste your time understanding it.

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.intro import showVideo
import numpy as np


def load_stylesheet(path):
    """This fnction loads the .qss stylesheet used for the GUI.
    Returns: read Stylesheet"""
    with open(path, "r") as f:
        return f.read()
    
def start_main():
    """This function starts the main window GUI."""
    window = MainWindow()
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    a = np.random.randint(0,100)
    if a == 11:
        intro = "assets/icons/rotoma.gif"
    else:
        intro = "assets/icons/intro.gif"
    app.setStyleSheet(load_stylesheet("assets/darkmode.qss"))
    intro = showVideo(intro, callback=start_main)
    intro.show()
    sys.exit(app.exec())