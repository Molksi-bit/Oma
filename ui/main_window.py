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
    #Menus
        file_menu = QMenu("&Datei", self)
        parameter_menu = QMenu("parameters", self)
        linear_menu = QMenu("linear", self)
        nonlinear_menu = QMenu("nonlinear", self)
    #Menu-actions
        open_action = QAction("Load", self)
        save_action = QAction("Save", self)
        saveas_action = QAction("Save as...", self)
        export_action = QAction("Export",self)

        parameter_action = QAction("parameters", self)

        linopt_action = QAction("open linopt", self)

        nonlinopt_action = QAction("open nonlinopt")
        
    #Adding everything
        file_menu.addAction(open_action)
        parameter_menu.addAction(parameter_action)
        linear_menu.addAction(linopt_action)
        nonlinear_menu.addAction(nonlinopt_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(parameter_menu)
        menu_bar.addMenu(linear_menu)
        menu_bar.addMenu(nonlinear_menu)
        self.setMenuBar(menu_bar)