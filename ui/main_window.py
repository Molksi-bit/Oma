from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QFrame,QStackedWidget, QSizePolicy
    )
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Qt

def load_stylesheet(path):
        with open(path,"r") as file :
            return file.read()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OMA")
        self.setMinimumSize(1200,800)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.views = {
            "lin" : self.create_lin_layout(),
            "parameters" : self.create_parameters_layout(),
        }
        for view in self.views.values():
            self.stacked.addWidget(view)

        
        self.create_menu()

    
    def create_menu(self):
        menu_bar = QMenuBar(self)
    #Menus
        file_menu = QMenu("&Datei", self)
        lattice_menu = QMenu("Lattice", self)
        linear_menu = QMenu("linear", self)
        nonlinear_menu = QMenu("nonlinear", self)
        settings_menu = QMenu("Settings",self)
    #Menu-actions
        open_action = QAction("Load", self)
        save_action = QAction("Save", self)
        saveas_action = QAction("Save as...", self)
        export_action = QAction("Export",self)

        edit_action  =QAction("Edit", self)
        parameter_action = QAction("parameters", self)
        parameter_action.triggered.connect(lambda: self.switch_view("parameters"))

        linopt_action = QAction("Linear design", self)
        linopt_action.triggered.connect(lambda: self.switch_view("lin"))

        nonlinopt_action = QAction("Nonlinear design",self)

        theme_action = QAction("change theme", self)
        
    #Adding everything
        file_menu.addActions([open_action,save_action,saveas_action,export_action])
        
        lattice_menu.addActions([edit_action,parameter_action])

        linear_menu.addActions([linopt_action])

        nonlinear_menu.addActions([nonlinopt_action])

        settings_menu.addActions([theme_action])

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(lattice_menu)
        menu_bar.addMenu(linear_menu)
        menu_bar.addMenu(nonlinear_menu)
        menu_bar.addMenu(settings_menu)

        # Shortcuts
        linopt_action.setShortcut("Ctrl+1")
        parameter_action.setShortcut("Ctrl+2")

        self.setMenuBar(menu_bar)

    def create_lin_layout(self):
        #Main Ansicht der Lineare Optik erstmal, vielleicht bessere erstansicht später
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        self.lattice_table = QTableWidget()
        self.lattice_table.setContentsMargins(0,0,0,0)
        self.lattice_table.setRowCount(16)
        self.lattice_table.setColumnCount(1)
        self.lattice_table.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.lattice_table.setFixedHeight(760)
        self.lattice_table.setFixedWidth(187)
        self.lattice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lattice_table.horizontalHeader().setVisible(False)
        self.lattice_table.setVerticalHeaderLabels(["Name", "Lenght", "Angle", "Abs. Angle", "Tune_x", "Tune_y","Chroma_x","Chroma_y",
                                                     "Mom. Comp.", "Energy","Damp. J_x", "Damp. J_y","E-loss", "E-Spread","Emit._x", "Emit._y" ])

        self.function_table =QTableWidget()
        self.function_table.setRowCount(7)
        self.function_table.setColumnCount(1)
        self.function_table.horizontalHeader().setVisible(False)
        self.function_table.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.function_table.setFixedHeight(760)
        self.function_table.setFixedWidth(175)
        self.function_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.function_table.setVerticalHeaderLabels(["s [m]","beta_x [m]","alpha_x","beta_y [m]","alpha_y","Disp [m]","Disp' "])

        self.plot_area  = QFrame( )
        self.plot_area.setObjectName("plotframe")
        self.plot_area.setMinimumSize(400, 400)

        main_layout.addWidget(self.lattice_table, 1)
        main_layout.addWidget(self.plot_area, 5)
        main_layout.addWidget(self.function_table, 1)

        main_widget.setLayout(main_layout)

        return main_widget

    def create_lattice_layout(self):
         pass
    
    def create_parameters_layout(self):
        widget = QWidget()
        layout = QVBoxLayout()
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Parameter", "Limit", "Wert", "Status"])
        table.setRowCount(3)

        self.limit_table = table  # falls du später darauf zugreifen willst

        self.limit_parameters = [
            {"name": "Energy", "limit": 2.5},
            {"name": "Dipolstrength", "limit": 1},
            {"name": "Quadrupolstrength", "limit": 80},
        ]

        for row, param in enumerate(self.limit_parameters):
            name_item = QTableWidgetItem(param["name"])
            name_item.setFlags(Qt.ItemIsEnabled)
            limit_item = QTableWidgetItem(str(param["limit"]))
            limit_item.setFlags(Qt.ItemIsEnabled)
            value_item = QTableWidgetItem("")
            status_item = QTableWidgetItem("-")
            status_item.setFlags(Qt.ItemIsEnabled)

            table.setItem(row, 0, name_item)
            table.setItem(row, 1, limit_item)
            table.setItem(row, 2, value_item)
            table.setItem(row, 3, status_item)

        table.cellChanged.connect(self.check_limits)

        layout.addWidget(table)
        widget.setLayout(layout)
        return widget
    

    def check_limits(self, row, column):
        if column != 2:
            return
        try:
            value = float(self.limit_table.item(row, 2).text())
        except ValueError:
            return

        name = self.limit_table.item(row, 0).text()
        limit = float(self.limit_table.item(row, 1).text())
        status_item = self.limit_table.item(row, 3)

        if value > limit:
            status_item.setText("❌")
            status_item.setForeground(QColor("red"))
            self.limit_violations[name] = {"value": value, "limit": limit}
        else:
            status_item.setText("✅")
            status_item.setForeground(QColor("green"))
            if name in self.limit_violations:
                del self.limit_violations[name]




    def create_nonlin_layout(self):
         widget = QWidget()
         layout = QVBoxLayout()

         
    def switch_view(self,name:str):
        if name in self.views:
            self.stacked.setCurrentWidget(self.views[name])
        else:
            print(f"Ansicht '{name}' nicht gefunden")