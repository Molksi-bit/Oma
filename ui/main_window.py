from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QFrame,QStackedWidget, QSizePolicy, QFileDialog,QLabel,QListWidget, QListWidgetItem,QMessageBox,
    QPushButton,QApplication,QScrollArea, QLineEdit, QScrollBar)
from PySide6.QtGui import QAction, QColor, QIcon
from PySide6.QtCore import Qt
from file_io.json_loader import load_file
from ui.plot_canvas import linear_plot, nonlinear_plot, calculate_nonlin, get_max_contribution,calculate_linear#, calculate_rdts
from matplotlib.figure import Figure
import os
import at
from at import Drift, Quadrupole, Sextupole, Dipole
import numpy as np

def load_stylesheet(path):
        with open(path,"r") as file :
            return file.read()


class MainWindow(QMainWindow):
    
    def __init__(self):
        """This function initializes the mainwindow of the GUI together with all variables for later use.
        Contains a dictionary for all diffrent views of the programm."""
        super().__init__()
        self.setWindowTitle("OMA")
        self.setMinimumSize(1200,800)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.views = {
            "home": self.create_home_layout(),
            "lin" : self.create_lin_layout(),
            "parameters" : self.create_parameters_layout(),
            "rdt": self.create_rdt_layout(),
            "chroma": self.create_chroma_layout(),
            "nonlin": self.create_nonlin_layout(),
            "mag_con": self.create_magnetcon_layout(),
            "editor" : self.create_lattice_layout()
            
        }
        for view in self.views.values():
            self.stacked.addWidget(view)
        self.lattices = {}
        self.selected_sections = {}
        self.nonlin_cache = {}
        self.lin_cache = {}
        self.needs_recalc = True
        self.active_plot = None
        self.saved_plots = []
        self.lattice_tables = {}  
        self.section_lists = {} 
        self.lattice_widgets = {}
        self.active_cell = None
        self.active_magnets = []
        
        self.create_menu()

    def lattice_change(self):
        """This function resets the marker, when the lattice was changed, so that the data from the cache has to
        be recalculated."""
        self.needs_recalc = True
    
    def create_menu(self):
        """This function creates the menu bar of the function. Furthemore it handles the actions triggered on
        click and sets Shortcuts for special actions."""
        menu_bar = QMenuBar(self)
    #Menus
        file_menu = QMenu("&Datei", self)
        lattice_menu = QMenu("Lattice", self)
        linear_menu = QMenu("Linear", self)
        nonlinear_menu = QMenu("Nonlinear", self)
        theme_menu = QMenu("Theme",self)
        plot_menu = QMenu("Plot", self)
        theory_menu = QMenu("Theory", self)
    #Menu-actions
        home_action = QAction(QIcon("assets/icons/haus.png"),"",self)
        home_action.setShortcut("Ctrl+H")
        home_action.setIconText("")
        home_action.triggered.connect(lambda: self.switch_view("home"))

        open_action = QAction("Load", self)
        open_action.triggered.connect(self.load_lattice_file)
        save_action = QAction("Save", self)
        saveas_action = QAction("Save as...", self)
        export_action = QAction("Export",self)

        edit_action  =QAction("Editor", self)
        edit_action.triggered.connect(lambda: self.switch_view("editor"))
        parameter_action = QAction("parameters", self)
        parameter_action.triggered.connect(lambda: self.switch_view("parameters"))

        linopt_action = QAction("Linear design", self)
        linopt_action.triggered.connect(lambda: self.switch_view("lin"))
        linopt_action.triggered.connect(lambda: self.plot_beta())

        nonlinopt_action = QAction("Nonlinear design",self)
        nonlinopt_action.triggered.connect(lambda: self.switch_view("nonlin"))
        nonlinopt_action.triggered.connect(lambda: self.plot_nonlin("chrom1"))
        rdts_action = QAction("RDTs",self)
        rdts_action.triggered.connect(lambda: self.switch_view("rdt"))
        magnet_contribution_action = QAction("Magnet contribution",self)
        magnet_contribution_action.triggered.connect(lambda:self.switch_view("mag_con"))
        magnet_contribution_action.triggered.connect(lambda:self.show_mag_contribution())
        chroma_action = QAction("Chromaticity", self)
        chroma_action.triggered.connect(lambda: self.switch_view("chroma"))

        light_action = QAction("Lightmode", self)
        light_action.triggered.connect(lambda: self.switch_theme("light"))
        dark_action = QAction("Darkmode", self)
        dark_action.triggered.connect(lambda: self.switch_theme("dark"))
        sepia_action = QAction("Sepiamode", self)
        sepia_action.triggered.connect(lambda: self.switch_theme("sepia"))
        highcon_action = QAction("High contrast", self)
        highcon_action.triggered.connect(lambda: self.switch_theme("highcon"))
        developer_action = QAction("Developer", self)
        developer_action.triggered.connect(lambda: self.switch_theme("developer"))


        save_plot_action = QAction("Save Plot",self)
        save_plot_action.triggered.connect(lambda: self.export_active_plot())
        save_all_plots_action = QAction("Save all Plots", self)
        save_all_plots_action.triggered.connect(lambda: self.export_all_plots())

        look_up_action = QAction("Look up", self)
        book_action = QAction("Book", self)
        research_action = QAction("Research", self)

        
    #Adding everything

        file_menu.addActions([open_action,save_action,saveas_action,export_action])
        
        lattice_menu.addActions([edit_action,parameter_action])

        linear_menu.addActions([linopt_action])

        nonlinear_menu.addActions([nonlinopt_action, rdts_action,magnet_contribution_action,chroma_action])

        theme_menu.addActions([light_action,dark_action,sepia_action,developer_action,highcon_action])

        plot_menu.addActions([save_plot_action, save_all_plots_action])

        menu_bar.addAction(home_action)
        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(lattice_menu)
        menu_bar.addMenu(linear_menu)
        menu_bar.addMenu(nonlinear_menu)
        menu_bar.addMenu(theme_menu)
        menu_bar.addMenu(plot_menu)

        # Shortcuts
        linopt_action.setShortcut("Ctrl+1")
        parameter_action.setShortcut("Ctrl+2")
        nonlinopt_action.setShortcut("Ctrl+3")
        open_action.setShortcut("Ctrl+l")
        home_action.setShortcut("Ctrl+h")
        save_plot_action.setShortcut("Ctrl+p")
        save_all_plots_action.setShortcut("Ctrl+shift+p")

        self.setMenuBar(menu_bar)

    def create_lin_layout(self):
        """This functions creates the layout of the linear plot view. """
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        fields = ["Name", "Lenght", "Angle", "Abs. Angle", "Qₓ", "Qᵧ","χₓ","χᵧ"] #"α", "Energy","Damp. Jₓ", "Damp. Jᵧ","E-loss", "E-Spread","εₓ", "εᵧ" ]
        self.lattice_table = QTableWidget()
        self.lattice_table.setContentsMargins(0,0,0,0)
        self.lattice_table.setRowCount(len(fields))
        self.lattice_table.setColumnCount(1)
        self.lattice_table.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.lattice_table.setFixedHeight(760)
        self.lattice_table.setFixedWidth(187)
        self.lattice_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.lattice_table.horizontalHeader().setVisible(False)
        self.lattice_table.setVerticalHeaderLabels(fields)
                                                     

        self.function_table =QTableWidget()
        self.function_table.setRowCount(8)
        self.function_table.setColumnCount(1)
        self.function_table.horizontalHeader().setVisible(False)
        self.function_table.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
        self.function_table.setFixedHeight(760)
        self.function_table.setFixedWidth(175)
        self.function_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.function_table.setVerticalHeaderLabels(["s [m]","βₓ [m]","αₓ","βᵧ [m]","αᵧ","Dₓ [m]","Dₓ' ","Magnet"])
        

        self.plot_area  = QVBoxLayout()

        self.plot_canvas_frame = QFrame()
        self.plot_canvas_layout = QVBoxLayout()
        self.plot_canvas_layout.setContentsMargins(0, 0, 0, 0)
        self.plot_canvas_frame.setLayout(self.plot_canvas_layout)
        
        self.placeholder = QLabel("No Lattice loaded")
        self.placeholder.setAlignment(Qt.AlignCenter)
        self.placeholder.setObjectName("placeholder")
        self.plot_canvas_layout.addWidget(self.placeholder)

        self.knob_widget = QWidget()
        self.knob_layout = QHBoxLayout()
        self.knob_widget.setLayout(self.knob_layout)

        self.plot_area.setContentsMargins(0, 0, 0, 0)
        self.plot_area.addWidget(self.plot_canvas_frame, 4)
        self.plot_area.addWidget(self.knob_widget, 1) 
        
        self.placeholder_frame = QFrame()
        self.placeholder_frame.setLayout(self.plot_area)
        self.placeholder_frame.setContentsMargins(0, 0, 0, 0)

        main_layout.addWidget(self.lattice_table, 1)
        main_layout.addWidget(self.placeholder_frame, 5)
        main_layout.addWidget(self.function_table, 1)

        main_widget.setLayout(main_layout)

        return main_widget

    def create_lattice_layout(self):
         """This function creates the layout for the view, where new lattices can be designed.
         ToDo: Bro just start to write it."""
         main_widget = QWidget()
         main_layout = QVBoxLayout()
        
         energy_widget = QWidget()
         energy_layout = QHBoxLayout()
         energy_label = QLabel("Energy = ")
         energy_entry = QLineEdit()
         xbutton = QPushButton("X")
         xbutton.clicked.connect(lambda: self.switch_view("home"))
         energy_entry.setPlaceholderText("E in GeV")

         adapting_widget = QWidget()
         adapting_layout = QHBoxLayout()
         adapting_widget.setLayout(adapting_layout)

         self.elements_widget = QFrame()
         self.elements_layout = QVBoxLayout()
         self.elements_widget.setLayout(self.elements_layout)

         self.segment_widget = QFrame()
         self.segment_layout = QVBoxLayout()
         self.segment_widget.setLayout(self.segment_layout)


         adapting_layout.addWidget(self.elements_widget)
         adapting_layout.addWidget(self.segment_widget)
         adapting_widget.setLayout(adapting_layout)

         energy_layout.addWidget(energy_label)
         energy_layout.addWidget(energy_entry)
         energy_layout.addWidget(xbutton)
         energy_widget.setLayout(energy_layout)


         main_layout.addWidget(energy_widget,1)
         main_layout.addWidget(adapting_widget,19)


         main_widget.setLayout(main_layout)

         return main_widget
    
    def create_parameters_layout(self):
        """This function creates the layout for the parameter view. Here an overview over special parameters 
        shall be given and limits can be set and checked."""
        widget = QWidget()
        layout = QHBoxLayout()
        text_field = QFrame()
        text_field_layout = QVBoxLayout()
        commentary = QLabel("Comments")
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Parameter", "Limit", "Value", "Status"])
        table.setRowCount(8)

        self.limit_table = table

        self.limit_parameters = [
            {"name": "Energy", "limit": 2.5},
            {"name": "Dipolstrength", "limit": 1},
            {"name": "Quadrupolstrength", "limit": 80},
            {"name": "Sextupolestrength", "limit": 240},
            {"name": "Magnetlength", "limit": 0.1},
            {"name": "Emittance", "limit": 0.100},
            {"name": "Mom. Comp.", "limit": 0.0001},
            {"name": "Total Length", "limit": 365}
            
            
        ]

        for row, param in enumerate(self.limit_parameters):
            name_item = QTableWidgetItem(param["name"])
            name_item.setFlags(Qt.ItemIsEnabled)
            limit_item = QTableWidgetItem(str(param["limit"]))
            value_item = QTableWidgetItem("")
            value_item.setFlags(Qt.ItemIsEnabled)
            status_item = QTableWidgetItem("-")
            status_item.setFlags(Qt.ItemIsEnabled)

            table.setItem(row, 0, name_item)
            table.setItem(row, 1, limit_item)
            table.setItem(row, 2, value_item)
            table.setItem(row, 3, status_item)

        table.cellChanged.connect(self.check_limits)

        text_field_layout.addWidget(commentary)
        text_field.setLayout(text_field_layout)
        layout.addWidget(table)
        layout.addWidget(text_field)
        widget.setLayout(layout)
        return widget
    

    def check_limits(self, row, column):
        """This function checks, whether the given lattice exceeds the limits set in the parameter view.
        ToDo: Adjust so that the megnet strenghts are checked and the table is adjustable just in the right
        entry fields."""
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
        """This function creates the layout for the home view. There lattices can be loaded and will be shown.
        ToDo: Change lattice expansion to switch between full and not expanded mode."""
    
        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        self.lattice_container_widget = QWidget()
        self.lattice_container_layout = QVBoxLayout()
        self.lattice_container_widget.setLayout(self.lattice_container_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.lattice_container_widget)

        layout.addWidget(scroll_area)

        widget.setLayout(layout)
        return widget


    def create_nonlin_layout(self):
        """This function creates the layout for the nonlinear view. Here the contributions to the chromaticity
        and momentum compaction are shown in different plots."""
        widget = QWidget()
        layout = QVBoxLayout()

        layout.setContentsMargins(0,0,0,0)

        button_area =QFrame()
        button_area.setObjectName("nonlinButtonArea")
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0,0,0,0)
        self.chroma1_button = QPushButton("X1")
        self.chroma1_button.clicked.connect(lambda: self.plot_nonlin("chrom1"))
        self.chroma1_quad_button = QPushButton("X1 | Quad")
        self.chroma1_quad_button.clicked.connect(lambda: self.plot_nonlin("chrom1_quad"))
        self.chroma1_sext_button = QPushButton("X1 | Sext")
        self.chroma1_sext_button.clicked.connect(lambda: self.plot_nonlin("chrom1_sext"))
        self.chroma2_button = QPushButton("X2")
        self.chroma2_button.clicked.connect(lambda: self.plot_nonlin("chrom2"))
        self.chroma2_quad_button = QPushButton("X2 | Quad")
        self.chroma2_quad_button.clicked.connect(lambda: self.plot_nonlin("chrom2_quad"))
        self.chroma2_sext_button = QPushButton("X2 | Sext")
        self.chroma2_sext_button.clicked.connect(lambda: self.plot_nonlin("chrom2_sext"))
        self.chroma2_oct_button = QPushButton("X2 | Oct")
        self.chroma2_oct_button.clicked.connect(lambda: self.plot_nonlin("chrom2_oct"))
        self.alpha0_button = QPushButton("α0")
        self.alpha0_button.clicked.connect(lambda: self.plot_nonlin("alpha0"))
        self.alpha1_button = QPushButton("α1")
        self.alpha1_button.clicked.connect(lambda: self.plot_nonlin("alpha1"))
        self.alpha1_1_button = QPushButton("α1_1")
        self.alpha1_1_button.clicked.connect(lambda: self.plot_nonlin("alpha1_1"))
        self.alpha1_2_button = QPushButton("α1_2")
        self.alpha1_2_button.clicked.connect(lambda: self.plot_nonlin("alpha1_2"))

        button_layout.addWidget(self.chroma1_button)
        button_layout.addWidget(self.chroma1_quad_button)
        button_layout.addWidget(self.chroma1_sext_button)
        button_layout.addWidget(self.chroma2_button)
        button_layout.addWidget(self.chroma2_quad_button)
        button_layout.addWidget(self.chroma2_sext_button)
        button_layout.addWidget(self.chroma2_oct_button)
        button_layout.addWidget(self.alpha0_button)
        button_layout.addWidget(self.alpha1_button)
        button_layout.addWidget(self.alpha1_1_button)
        button_layout.addWidget(self.alpha1_2_button)
        button_layout.setSpacing(20)
        button_area.setLayout(button_layout)

        self.bottom_frame = QFrame()
        self.bottom_layout = QHBoxLayout()
        self.bottom_layout.setContentsMargins(0,0,0,0)

        self.right_frame = QFrame()
        self.right_layout = QVBoxLayout()
        self.right_frame.setContentsMargins(0,0,0,0)

        self.right_frame.setLayout(self.right_layout)
        

        fields = ["X1_totx","X1_toty","α","Magnet","Value", "Position [m]", "Field"]
        self.nonlin_table = QTableWidget()
        self.nonlin_table.setContentsMargins(0,0,0,0)
        self.nonlin_table.setColumnCount(1)
        self.nonlin_table.setRowCount(len(fields))
        self.nonlin_table.horizontalHeader().setVisible(False)
        self.nonlin_table.setVerticalHeaderLabels(fields)
        
        self.nonlin_values_table = QTableWidget()
        self.nonlin_values_table.setColumnCount(1)
        self.nonlin_values_table.setRowCount(3)
        self.nonlin_values_table.horizontalHeader().setVisible(False)
        self.nonlin_values_table.setVerticalHeaderLabels(["s","2", "3"])


        self.nonlin_plot_area = QFrame()
        self.nonlin_plot_area.setObjectName("nonlinPlotArea")
        self.nonlin_plot_layout = QVBoxLayout()
        self.nonlin_plot_layout.setContentsMargins(0,0,0,0)
        self.nonlin_plot_area.setLayout(self.nonlin_plot_layout)

        self.right_layout.addWidget(self.nonlin_table)
        self.right_layout.addWidget(self.nonlin_values_table)

        self.bottom_layout.addWidget(self.nonlin_plot_area,5)
        self.bottom_layout.addWidget(self.right_frame)
        self.bottom_frame.setLayout(self.bottom_layout)

        layout.addWidget(button_area,1)
        layout.addWidget(self.bottom_frame,8)
        widget.setLayout(layout)
        return widget

    def create_rdt_layout(self):
        """This function creates the layout for the Resonance driving term (RDTs) view.
        ToDo: replace the unicode"""
        widget = QWidget()
        layout = QHBoxLayout()

        tables = QVBoxLayout()
        layout.addLayout(tables,1)
        
        rdt_label1 = QLabel("1st Order Chromatic RDTs")
        self.rdt_table1 = QTableWidget()
        self.rdt_table1.setRowCount(5)
        self.rdt_table1.setColumnCount(1)
        self.rdt_table1.horizontalHeader().setVisible(False)
        self.rdt_table1.setVerticalHeaderLabels(["H\u2081\u2081\u2080\u2080\u2081",
                                                 "H\u2080\u2080\u2081\u2081\u2081",
                                                 "H\u2082\u2080\u2080\u2080\u2081",
                                                 "H\u2080\u2080\u2082\u2080\u2081",
                                                 "H\u2081\u2080\u2080\u2080\u2082"
                                                 ])
        self.rdt_table1.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        rdt_label2 = QLabel("1st Order geometric RDTs")
        self.rdt_table2 = QTableWidget()
        self.rdt_table2.setRowCount(5)
        self.rdt_table2.setColumnCount(1)
        self.rdt_table2.horizontalHeader().setVisible(False)
        self.rdt_table2.setVerticalHeaderLabels(["H\u2082\u2081\u2080\u2080\u2080",
                                                 "H\u2083\u2080\u2080\u2080\u2080",
                                                 "H\u2081\u2080\u2081\u2081\u2080",
                                                 "H\u2081\u2080\u2080\u2082\u2080",
                                                 "H\u2081\u2080\u2082\u2080\u2080"])
        self.rdt_table2.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        plot = QFrame()
        layout.addWidget(plot,3)
        tables.addWidget(rdt_label1)
        tables.addWidget(self.rdt_table1)
        tables.addWidget(rdt_label2)
        tables.addWidget(self.rdt_table2)

        widget.setLayout(layout)
        return widget


    def create_magnetcon_layout(self):
        """I dont know if this is still necessary but im t lazy to delete it."""
        wrapper = QWidget()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0,0,0,0)

        self.magnetcon_container = QWidget()
        self.magnetcon_container_layout = QVBoxLayout()
        self.magnetcon_container_layout.setContentsMargins(0,0,0,0)
        self.magnetcon_container.setLayout(self.magnetcon_container_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.magnetcon_container)
        view_label = QLabel("Magnet Contribution")



        wrapper_layout.addWidget(view_label)
        wrapper_layout.addWidget(scroll_area)
        wrapper.setLayout(wrapper_layout)


        return wrapper

    def create_omaedit_layout(self):
        """This function creates a diffrent layout, where a new lattice can be designed in an OPA related style.
        ToDo: Well this function looks great so far just leave it as it is."""
        pass   

    def load_lattice_file(self):
        """This function starts the loading of an lattice file. It opens the Dialogue window and updates the
        lattice_data variable."""
        file_path, _ = QFileDialog.getOpenFileName(self,"Datei öffnen", "", "JSON Files (*.json);; OPA Files (*.opa)")
        if file_path:
            sections, meta, elements = load_file(file_path)
            name = os.path.splitext(os.path.basename(file_path))[0]

        self.lattices[name] = {"sections": sections,
                             "meta": meta,
                             "elements": elements}
        self.show_lattice(name,sections,meta)
            

    def switch_view(self,name:str):
        """This function handles the view change."""
        if name in self.views:
            self.stacked.setCurrentWidget(self.views[name])
        else:
            print(f"Ansicht '{name}' nicht gefunden")

    def show_lattice(self,name,sections,meta):
        """This function creates a table containing the sections of an loaded lattice:
        ToDo: Prepare this boy for the introduction of multilatticing. Set a standard for cell selected to 
        be the first of the sections."""

        wrapper_frame = QFrame()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0,0,0,0)

        header = QHBoxLayout()
        title = QLabel(f"Lattice: {name}")
        wrapper_layout.addWidget(title)
        delete_btn = QPushButton("X")
        delete_btn.setFixedSize(45, 24)
        delete_btn.setToolTip("Lattice löschen")
        delete_btn.clicked.connect(lambda: self.remove_lattice_frame(name))

        header.addWidget(title)
        header.addStretch()
        header.addWidget(delete_btn)
        wrapper_layout.addLayout(header)

        
        content_layout = QHBoxLayout()

        
        param_table = QTableWidget()
        fields = ["name", "energy_GeV", "emittance_m_rad", "horizontal_tune", "vertical_tune",
                "natural_chromaticity_x", "natural_chromaticity_y", "rf_frequency_MHz", "rf_voltage_kV"]
        param_table.setColumnCount(1)
        param_table.setRowCount(len(fields))
        param_table.setVerticalHeaderLabels(fields)
        param_table.horizontalHeader().setVisible(False)
        for row, key in enumerate(fields):
            value = meta.get(key, "")
            item = QTableWidgetItem(str(value))
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            param_table.setItem(row, 0, item)

        
        section_layout = QVBoxLayout()
        section_table = QTableWidget()
        section_table.setColumnCount(4)
        section_table.setRowCount(len(sections) // 4 + 1)
        section_table.horizontalHeader().setVisible(False)
        section_table.verticalHeader().setVisible(False)
        
        for index, section in enumerate(sections.keys()):
            row = index // 4
            col = index % 4
            item = QTableWidgetItem(section)
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            section_table.setItem(row, col, item)

        expansion_list = QListWidget()
        expansion_list.setFlow(QListWidget.LeftToRight)
        expansion_list.setWrapping(True)
        expansion_list.setFixedHeight(80)

        section_layout.addWidget(section_table, 3)
        section_layout.addWidget(expansion_list, 1)

        
        content_layout.addWidget(param_table, 1)
        content_layout.addLayout(section_layout, 3)
        wrapper_layout.addLayout(content_layout)
        wrapper_frame.setLayout(wrapper_layout)

        
        self.lattice_tables[name] = section_table
        self.section_lists[name] = expansion_list
        self.lattice_widgets[name] = wrapper_frame
        section_table.cellClicked.connect(lambda r, c, ln=name: self.display_section_elements(r, c, ln))
        section_table.cellClicked.connect(lambda row, col,name = name:self.on_section_cell_clicked(row,col,name))

        
        self.lattice_container_layout.addWidget(wrapper_frame)

    def remove_lattice_frame(self, name):
        frame = self.lattice_widgets.pop(name, None)
        if frame:
            frame.setParent(None)
        self.lattices.pop(name,None)
    def display_section_elements(self,row,col, lattice_name):
        """This function shows lattice expansion in the bottom of the home view. It adds Tooltips to each
        element showing their parameters."""
        table = self.lattice_tables[lattice_name]
        item = table.item(row,col)
        if not item:
            return
        
        section_name = item.text()
        section_elements = self.lattices[lattice_name]["elements"].get(section_name, [])
        list_widget = self.section_lists[lattice_name]
        list_widget	.clear()

        for element in section_elements:

            tooltip = f"Typ: {element.__class__.__name__}\nLänge: {element.Length:.3f} m"
            if hasattr(element, "K") :#and element.K != 0
                tooltip += f"\nk1: {element.K:.3f}"
            if hasattr(element, "H"):#and  element.H != 0
                tooltip += f"\nk2: {element.H:.3f}"
            if hasattr(element,"BendingAngle"):
                tooltip += f"\nangle: {element.BendingAngle:.3f}"

            item = QListWidgetItem(element.FamName)
            item.setToolTip(tooltip)
            item.setData(Qt.UserRole, element)
            list_widget.addItem(item)

    def create_chroma_layout(self):
        """This function creates the layout for the chromaticity layout.
        ToDo: replace the unicode here aswell."""
        widget = QWidget()
        layout = QHBoxLayout()
        Chroma_functions = QVBoxLayout()
        sextupoles = QVBoxLayout()
        self.chroma_table = QTableWidget()
        self.chroma_table.setColumnCount(1)
        self.chroma_table.setRowCount(7)
        self.chroma_table.horizontalHeader().setVisible(False)
        self.chroma_table.setVerticalHeaderLabels(["Chrom\u2093 lin",
                                                  "Chrom\u2094 lin",
                                                  "Chrom\u2093 sqr",
                                                  "Chrom\u2094 sqr",
                                                  "Chrom\u2093 cub",
                                                  "Chrom\u2094 cub",
                                                  "summed sextupolstrength"])

        self.sextupole_table = QTableWidget()
        self.sextupole_table.setColumnCount(2)
        self.sextupole_table.setRowCount(2)
        self.sextupole_table.horizontalHeader().setVisible(False)
        self.sextupole_table.verticalHeader().setVisible(False)


        Chroma_functions.addWidget(self.chroma_table)
        sextupoles.addWidget(self.sextupole_table)

        layout.addLayout(Chroma_functions,1)
        layout.addLayout(sextupoles,1)
        widget.setLayout(layout)
        return widget
    
    def plot_beta(self):
        """This function plots the canvas of the linear functions and updates the linear cache.
        ToDo: update the linear cache duhhh"""
        data_list = []
        elements_list =[]
        labels= []
        if not self.lattices or not self.selected_sections:
            print(self.selected_sections)
            return
        for lattice_name,lattice_data in self.lattices.items():
            section = self.selected_sections.get(lattice_name)
            if not section:
                continue
            if lattice_name not in self.lin_cache:
                self.lin_cache[lattice_name] = {}
            if section not in self.lin_cache[lattice_name] or self.needs_recalc:
                elements = self.lattices[lattice_name]["elements"].get(section)
                data = calculate_linear(elements)
                self.lin_cache[lattice_name][section] = data
                self.needs_recalc = False
            else:
                data = self.lin_cache[lattice_name][section]
                elements = self.lattices[lattice_name]["elements"].get(section)
            data_list.append(data)
            elements_list.append(elements)
            labels.append(lattice_name)
        canvas = linear_plot(data_list,elements_list,labels=labels, callback= self.update_lin_table)
        self.lattice_table.setItem(1,0,QTableWidgetItem(str(round(max(data["s"]),3))))
        self.lattice_table.setItem(2,0,QTableWidgetItem(str(round(data["angle"],3))))
        self.lattice_table.setItem(3,0,QTableWidgetItem(str(round(data["abs_angle"],3))))
        self.lattice_table.setItem(4,0,QTableWidgetItem(str(round(data["tunes"][0],3))))
        self.lattice_table.setItem(5,0,QTableWidgetItem(str(round(data["tunes"][1],3))))
        self.lattice_table.setItem(6,0,QTableWidgetItem(str(round(data["chroma"][0],3))))
        self.lattice_table.setItem(7,0,QTableWidgetItem(str(round(data["chroma"][1],3))))
                                   
        if isinstance(canvas.figure, Figure):
            self.active_plot = canvas.figure
            self.saved_plots.append({
            "figure": canvas.figure,  
            "type": "linear",       
            "section": labels
        })
        for i in reversed(range(self.plot_canvas_layout.count())):
            widget = self.plot_canvas_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.plot_canvas_layout.addWidget(canvas)
            

    def plot_nonlin(self,function):
        """This funtion plots the canvas of the nonlinear functions and updates the nonlinear cache."""
        if not self.lattices or not self.selected_sections:
            return
        data_list = []
        elements_list =[]
        labels= []
        for lattice_name,lattice_data in self.lattices.items():
            section = self.selected_sections.get(lattice_name)
            if not section:
                continue
            if lattice_name not in self.nonlin_cache:
                self.nonlin_cache[lattice_name] = {}
            if section not in self.nonlin_cache or self.needs_recalc:
                elements = self.lattices[lattice_name]["elements"].get(section)
                data = calculate_nonlin(elements)
                self.nonlin_cache[lattice_name][section] = data
                self.needs_recalc =False
            else:
                data = self.nonlin_cache[lattice_name][section]
                elements = self.lattices[lattice_name]["elements"].get(section)
            data_list.append(data)
            elements_list.append(elements)
            labels.append(lattice_name)
        canvas = nonlinear_plot(data_list,function,elements_list,labels, callback=self.update_nonlin_table)
        if isinstance(canvas.figure, Figure):
            self.active_plot = canvas.figure
            self.saved_plots.append({
                "figure": canvas.figure,  
                "type": function,       
                "section": self.selected_sections
            })
        magnets = get_max_contribution(data, function,elements)
        for i,value in enumerate(magnets[0]):
            item = QTableWidgetItem(str(value))
            self.nonlin_table.setItem(i+3,0,item)
        Values = data_list[0]["chrom1_tot"][0]+data_list[0]["alpha1_tot"][0]
        for i,value in enumerate(Values):
            item = QTableWidgetItem(str(value))
            self.nonlin_table.setItem(i,0,item)
        for i in reversed(range(self.nonlin_plot_layout.count())):
            widget = self.nonlin_plot_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.nonlin_plot_layout.addWidget(canvas)


    def on_section_cell_clicked(self,row,col,name):
        """This function handles the selection of cells in the home layout used for the plotting."""
        item = self.lattice_tables[name].item(row,col)
        if not item:
            return
        
        self.selected_sections[name] = item.text()
        

    def export_active_plot(self):
        """This function export the active plot as png or pdf.
        ToDo: Other file types ?"""
        if hasattr(self, "active_plot") and self.active_plot:
            file_path, _ = QFileDialog.getSaveFileName(self, "Plot speichern", "", "PNG (*.png);;PDF (*.pdf)")
            if file_path:
                self.active_plot.savefig(file_path, dpi=300)
        else:
            QMessageBox.warning(self, "Fehler", "Kein aktiver Plot vorhanden.")

    def export_all_plots(self):
        """This function exports all generated plots in a seperated folder.
        ToDo: png or pdf selection"""
        if not self.saved_plots:
            QMessageBox.warning(self, "Keine Plots", "Es wurden noch keine Plots generiert.")
            return

        folder = QFileDialog.getExistingDirectory(self, "Exportverzeichnis wählen")
        if not folder:
            return

        for i, plot_data in enumerate(self.saved_plots):
            fig = plot_data["figure"]
            section = plot_data.get("section", f"plot_{i}")
            plot_type = plot_data.get("type", "plot")
            filename = f"{i:02d}_{section}_{plot_type}.png"
            save_path = os.path.join(folder, filename)
            fig.savefig(save_path, dpi=300)
        
        QMessageBox.information(self, "Export abgeschlossen", f"{len(self.saved_plots)} Plots gespeichert.")

        
    def clear_saved_plots(self):
        """This function will clear the saved_plots variable if needed."""
        self.saved_plots.clear()

    def update_lin_table(self, x, values:dict):
        """This function handles the updating of the values in the table of the linear plot."""
        magnet = values["magnet"]
        values = {k: v for k, v in values.items() if k != "magnet"}
        for i, (name,val) in enumerate(values.items()):
            if isinstance(val,float):
                item = QTableWidgetItem(f"{val:.4f}")
            else:
                item = QTableWidgetItem(val)
            item.setFlags(Qt.ItemIsEnabled)
            self.function_table.setItem(i, 0 , item)
        magnet_view = self.create_magnet_overview(magnet)
        self.knob_layout.addWidget(magnet_view)
        

    def update_nonlin_table(self, x, values:dict, function):
        """This function handles the updating of the values in the nonlinear function table."""
        functions = {
                 "chrom1": ["X1ₓ","X1ᵧ"],
                 "chrom1_quad": ["X1Qₓ","X1Qᵧ"],
                 "chrom1_sext": ["X1Sₓ","X1Sᵧ"],
                 "chrom2":["X2ₓ","X2ᵧ"],
                 "chrom2_quad":["X2Qₓ","X2Qᵧ"],
                 "chrom2_sext":["X2Sₓ","X2Sᵧ"],
                 "chrom2_oct":["X2Oₓ","X2Oᵧ"],
                 "alpha0": ["α0"],
                 "alpha1": ["α1"],
                 "alpha1_1": ["α1 ds"],
                 "alpha1_2": [ "α1 dE"]
                 }
        self.nonlin_values_table.setRowCount(len(functions[function])+1)
        self.nonlin_values_table.setVerticalHeaderLabels(["s"]+functions[function])
        for i, (name,val) in enumerate(values.items()):
            item = QTableWidgetItem(f"{val:.4f}")
            item.setFlags(Qt.ItemIsEnabled)
            self.nonlin_values_table.setItem(i, 0 , item)
            
    def show_mag_contribution(self):
        """This function creates the Tables for presentation in the Magnet contribution view."""
        if not self.selected_sections:
            return
        self.clear_layout(self.magnetcon_container_layout)
        wrapper_frame = QFrame()
        wrapper_layout = QVBoxLayout()
        wrapper_layout.setContentsMargins(0,0,0,0)

        fields = ["X1","X1S","X2", "X2S","A0","A11", "A12"]
        
        

        for lattice_name, section_name in self.selected_sections.items():
            title = QLabel(f"Lattice: {lattice_name} | Section: {section_name}")
            wrapper_layout.addWidget(title)
            table = QTableWidget()
            table.setColumnCount(len(fields))
            table.setHorizontalHeaderLabels(fields)
            elements = self.lattices[lattice_name]["elements"][section_name]
            header_labels =[]
            for element in elements:
                if not isinstance(element,at.Drift):
                    header_labels.append(element.FamName)
            table.setRowCount(len(header_labels))
            table.setVerticalHeaderLabels(header_labels)
            wrapper_layout.addWidget(table)

            #calculate_rdts(elements)
        wrapper_frame.setLayout	(wrapper_layout)
        self.magnetcon_container_layout.addWidget(wrapper_frame)



    def switch_theme(self,mode):
        """This function handles the switch of themes, which are present in the assets folder."""
        themes = {"light":"assets/lightmode.qss",
                  "dark":"assets/darkmode.qss" ,
                  "developer":"assets/developer.qss",
                  "sepia":"assets/sepiamode.qss",
                  "highcon":"assets/high_contrast.qss"}
        
        with open(themes[mode], "r") as file:
            style= file.read()
            QApplication.instance().setStyleSheet(style)

    
    def clear_layout(self,layout):

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            child_layout = item.layout()

            if widget is not None:
                widget.setParent(None)
            elif child_layout is not None:
                self.clear_layout(child_layout)

    def load_editor(self):
        for element in self.lattices[0]:
            label = QWidget()




    def plot_rdts(self,lattice):
        pass

    def create_magnet_overview(self,magnet):
        main_widget = QFrame()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)


        topper_widget = QWidget()
        topper_layout = QHBoxLayout(topper_widget)
        topper_layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(magnet.FamName)
        xbutton = QPushButton("X")
        xbutton.setFixedWidth(40)
        xbutton.clicked.connect(lambda: self.remove_overview(main_widget))

        topper_layout.addWidget(label)
        topper_layout.addWidget(xbutton)


        scrollbar = QScrollBar(Qt.Horizontal)
        value_label = QLineEdit()
        stepsize = QLineEdit("0.01")
        stepsize.setFixedWidth(80)

        main_layout.addWidget(topper_widget)
        main_layout.addWidget(scrollbar)
        main_layout.addWidget(value_label)
        main_layout.addWidget(stepsize)


        main_widget.setLayout(main_layout)
        scale = lambda x: x

        if isinstance(magnet, Dipole):
            raw_value = getattr(magnet, "BendingAngle", 0.0)
            initial_value = np.degrees(raw_value)
            attr_name = "BendingAngle"
            value_range = (-45, 45)
        
        elif isinstance(magnet, Quadrupole):
            initial_value = getattr(magnet, "K", 0.0)
            attr_name = "K"
            value_range = (-10, 10)

        elif isinstance(magnet, Sextupole):
            initial_value = getattr(magnet, "H", 0.0)
            attr_name = "H"
            value_range = (-100, 100)

        elif isinstance(magnet, Drift):
            initial_value = getattr(magnet, "Length", 0.0)
            attr_name = "Length"
            value_range = (0.01, 20)
        else:
            value_label.setText("–")
            value_label.setEnabled(False)
            scrollbar.setEnabled(False)
            stepsize.setEnabled(False)
            return main_widget
        value_label.setText(f"{initial_value:.3f}")
        step_init = float(stepsize.text())
        scrollbar.setMinimum(int((value_range[0] - initial_value) / step_init))
        scrollbar.setMaximum(int((value_range[1] - initial_value) / step_init))


        def on_scroll(value):
            try:
                step = float(stepsize.text())
            except ValueError:
                stepsize.setText("0.01")
                step = 0.01
            new_val = initial_value + value * step
            value_label.setText(f"{new_val:.4f}")
            setattr(magnet, attr_name, scale(new_val))
            self.needs_recalc =True
            self.plot_beta()
        def on_edit():
            try:
                val = float(value_input.text())
            except ValueError:
                return
            setattr(magnet, attr_name, scale(val))
            self.needs_recalc = True
            self.plot_beta()
        scrollbar.valueChanged.connect(on_scroll)
        value_label.editingFinished.connect(on_edit)
        return main_widget
    
    def remove_overview(self, widget):
        self.knob_layout.removeWidget(widget)
        widget.deleteLater()

    def create_value_input(self,magnet):
        if  isinstance(magnet, Dipole):
            angle_deg = magnet.t * (180 / 3.141592653589793)
            lineedit = QLineEdit(f"{angle_deg:.4f}")
            lineedit.setToolTip("Biegewinkel in Grad")
        elif isinstance(magnet, Quadrupole):
            lineedit = QLineEdit(f"{magnet.K:.4f}")
            lineedit.setToolTip("Quadrupol-Stärke K1")
        elif isinstance(magnet, Sextupole):
            lineedit = QLineEdit(f"{magnet.H:.4f}")
            lineedit.setToolTip("Sextupol-Stärke K2")
        elif isinstance(magnet, Drift):
            lineedit = QLineEdit(f"{magnet.Length:.4f}")
            lineedit.setToolTip("Driftlänge")
        else:
            lineedit = QLineEdit("–")
            lineedit.setEnabled(False)

        lineedit.setFixedWidth(80)
        return lineedit