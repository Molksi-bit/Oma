from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QAction
    )


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OMA")
        self.setMinimumSize(1200,800)


        self.create_menu
        self.create_main_layout

    def create_menu(self):
        menu_bar = QMenuBar(self)
        file_menu = QMenu("&Datei", self)
        linear_menu = QMenu("linear", self)
        nonlinear_menu = QMenu("nonlinear", self)
        open_action = QAction("load Lattice", self)
        file_menu.addAction(open_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(linear_menu)
        menu_bar.addMenu(nonlinear_menu)
        self.setMenuBar(menu_bar)