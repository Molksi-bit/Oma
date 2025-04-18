from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QFrame,QStackedWidget, QSizePolicy, QFileDialog,QLabel,QListWidget, QListWidgetItem
    )
from PySide6.QtGui import QAction, QColor
from PySide6.QtCore import Qt
from file_io.json_loader import load_file

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
            "home": self.create_home_layout(),
            "lin" : self.create_lin_layout(),
            "parameters" : self.create_parameters_layout(),
            
        }
        for view in self.views.values():
            self.stacked.addWidget(view)

        
        self.create_menu()

    
    def create_menu(self):
        menu_bar = QMenuBar(self)
    #Menus
        home_menu = QMenu("home",self)
        file_menu = QMenu("&Datei", self)
        lattice_menu = QMenu("Lattice", self)
        linear_menu = QMenu("linear", self)
        nonlinear_menu = QMenu("nonlinear", self)
        settings_menu = QMenu("Settings",self)
    #Menu-actions
        home_action = QAction("Startseite",self)
        home_action.setShortcut("Ctrl+H")
        home_action.triggered.connect(lambda: self.switch_view("home"))

        open_action = QAction("Load", self)
        open_action.triggered.connect(self.load_lattice_file)
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
        home_menu.addActions([home_action])

        file_menu.addActions([open_action,save_action,saveas_action,export_action])
        
        lattice_menu.addActions([edit_action,parameter_action])

        linear_menu.addActions([linopt_action])

        nonlinear_menu.addActions([nonlinopt_action])

        settings_menu.addActions([theme_action])

        menu_bar.addMenu(home_menu)
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
        self.lattice_table.setVerticalHeaderLabels(["Name", "Lenght", "Angle", "Abs. Angle", "Tune\u2093", "Tune\u2094","Chroma\u2093","Chroma\u2094",
                                                     "Mom. Comp.", "Energy","Damp. J\u2094", "Damp. J\u2094","E-loss", "E-Spread","\u03B5\u2093", "\u03B5\u2094" ])
        self.function_table =QTableWidget()
        self.function_table.setRowCount(7)
        self.function_table.setColumnCount(1)
        self.function_table.horizontalHeader().setVisible(False)
        self.function_table.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.function_table.setFixedHeight(760)
        self.function_table.setFixedWidth(175)
        self.function_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.function_table.setVerticalHeaderLabels(["s [m]","\u03B2\u2093 [m]","\u03B1\u2093","\u03B2\u2094 [m]","\u03B1\u2094","Disp [m]","Disp' "])
        

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
        table.setRowCount(8)

        self.limit_table = table  # falls du später darauf zugreifen willst

        self.limit_parameters = [
            {"name": "Energy", "limit": 2.5},
            {"name": "Dipolstrength", "limit": 1},
            {"name": "Quadrupolstrength", "limit": 80},
            {"name": "Sextupolestrength", "limit": 240},
            {"name": "Magnetlength", "limit": 10},
            {"name": "Emittance", "limit": 0.100},
            {"name": "Mom. Comp.", "limit": 0.0001},
            {"name": "Total Length", "limit": 365}
            
            
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

    def create_home_layout(self):
        widget = QWidget()
        layout = QHBoxLayout()
        right_side = QVBoxLayout()
        self.param_table = QTableWidget()
        self.param_table.setColumnCount(1)
        parameters = ["Name","Energy", "Emittance" ]
        self.param_table.setRowCount(len(parameters))
        self.param_table.setVerticalHeaderLabels(parameters)
        self.param_table.horizontalHeader().setVisible(False)

        self.lattice_table_widget = QTableWidget()
        self.lattice_table_widget.setColumnCount(4)
        self.lattice_table_widget.setRowCount(1)
        self.lattice_table_widget.horizontalHeader().setVisible(False)
        self.lattice_table_widget.verticalHeader().setVisible(False)
        self.lattice_table_widget.cellClicked.connect(self.display_section_elements)

        self.section_element_list = QListWidget()
        self.section_element_list.setFlow(QListWidget.LeftToRight)
        self.section_element_list.setWrapping(True)
        
        right_side.addWidget(self.lattice_table_widget,3)
        right_side.addWidget(self.section_element_list,1)
        layout.addWidget(self.param_table,1)
        layout.addLayout(right_side,3)
        widget.setLayout(layout)
        return widget


    def create_nonlin_layout(self):
         widget = QWidget()
         layout = QVBoxLayout()

    def load_lattice_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self,"Datei öffnen", "", "JSON Files (*.json);; OPA Files (*.opa)")
        if file_path:
            sections, meta, elements = load_file(file_path)

        self.lattice_data = {"sections": sections,
                             "meta": meta,
                             "elements": elements}
        self.show_lattice(sections,meta)
            

    def switch_view(self,name:str):
        if name in self.views:
            self.stacked.setCurrentWidget(self.views[name])
        else:
            print(f"Ansicht '{name}' nicht gefunden")

    def show_lattice(self,sections,meta):
        table = self.lattice_table_widget
        table.clearContents()
        table.setRowCount(len(sections)//4 +1)
        section_names = sections.keys()
        for index,section in enumerate(section_names):
            row =index//4
            col = index %4
            name_item = QTableWidgetItem(section)
            name_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

            table.setItem(row,col,name_item)


        param_table = self.param_table
        param_table.clearContents()
        values= meta["name"], meta["energy_GeV"], meta["emittance_m_rad"]
        for row,value in enumerate(values):
            item = QTableWidgetItem(str(value))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            param_table.setItem(row,0,item)
            
    def display_section_elements(self,row,col):
        item = self.lattice_table_widget.item(row,col)
        if not item:
            return
        
        section_name = item.text()
        section_elements = self.lattice_data["elements"].get(section_name, [])

        self.section_element_list.clear()
        for element in section_elements:

            tooltip = f"Typ: {element.__class__.__name__}\nLänge: {element.length:.3f} m"
            if hasattr(element, "k1"):
                tooltip += f"\nk1: {element.k1:.3f}"
            if hasattr(element, "k2"):
                tooltip += f"\nk2: {element.k2:.3f}"
            if hasattr(element,"angle"):
                tooltip += f"\nangle: {element.angle:.3f}"
            item = QListWidgetItem(element.name)
            item.setToolTip(tooltip)
            item.setData(Qt.UserRole, element)
            self.section_element_list.addItem(item)