import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def load_stylesheet(path):
    with open(path, "r") as f:
        return f.read()
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet("assets/darkmode.qss"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())