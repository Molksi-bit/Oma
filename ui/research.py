from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QFrame,QStackedWidget, QSizePolicy, QFileDialog,QLabel,QListWidget, QListWidgetItem,QMessageBox,
    QPushButton,QApplication,QScrollArea, QLineEdit, QScrollBar,QStyle, QComboBox)
import os
from PySide6.QtGui import QAction, QColor, QIcon
from PySide6.QtCore import Qt
import webbrowser
import requests
import feedparser
from file_io.user_data import UserDataManager



class ResearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Research")
        self.setMinimumSize(600,400)
        self.user_data = UserDataManager()
        
        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.views = {
            "home" : self.create_home_layout(),
            "history": self.create_history_Layout(),
            "settings": self.create_settings_Layout()
        }
        for view in self.views.values():
            self.stacked.addWidget(view)
        self.create_menu()

    def create_menu(self):
        menu_bar = QMenuBar(self)
 
        home_action = QAction(QIcon("assets/icons/home.svg"),"",self)
        home_action.setShortcut("Ctrl+H")
        home_action.triggered.connect(lambda: self.switch_view("home"))

        history_action = QAction("History",self)
        history_action.setShortcut("Ctrl+Shift+H")
        history_action.triggered.connect(lambda: self.switch_view("history"))

        settings_action = QAction("Settings",self)
        settings_action.setShortcut("Ctrl+S")
        settings_action.triggered.connect(lambda: self.switch_view("settings"))

        

        menu_bar.addAction(home_action)
        menu_bar.addAction(history_action)
        menu_bar.addAction(settings_action)

        self.setMenuBar(menu_bar)


    def switch_view(self,name:str):
        """This function handles the view change."""
        if name in self.views:
            self.stacked.setCurrentWidget(self.views[name])
        else:
            print(f"Ansicht '{name}' nicht gefunden")

    def create_home_layout(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10,10,10,0)

        searchfield = QWidget()
        searchfield_layout = QHBoxLayout()

        self.label = QLabel("Keywords:")
        searchfield_layout.addWidget(self.label)

        self.entry_field = QLineEdit()
        self.entry_field.returnPressed.connect(self.search_paper)
        searchfield_layout.addWidget(self.entry_field)

        self.search_button = QPushButton("")
        icon = self.search_button.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay)
        self.search_button.setIcon(icon)
        self.search_button.clicked.connect(self.search_paper)
        searchfield_layout.addWidget(self.search_button)

        searchfield.setLayout(searchfield_layout)
        main_layout.addWidget(searchfield)

        self.result_list = QListWidget()
        main_layout.addWidget(self.result_list)

        main_widget.setLayout(main_layout)

        return main_widget

    def search_paper(self):
        entry = self.entry_field.text()
        self.user_data.add_search_term(entry)
        self.result_list.clear()
        theme = "acc-ph"
        if not entry:
            return
        
        clean_entry = entry.replace(" ","+")
        url = f"http://export.arxiv.org/api/query?search_query=all:{clean_entry}+AND+cat:physics.{theme}&start=0&max_results=10"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler: HTTP {response.status_code}")
            return []
        feed = feedparser.parse(response.text)
        results = []
        for entry in feed.entries:
            arxiv_id = entry.id.split('/abs/')[-1]
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            results.append({
                "title": entry.title,
                "published": entry.published[:4],
                "link": entry.link,
                "pdf": pdf_link
            })
        for result in results:
            item = QListWidgetItem(f"{result['title']} ({result['published']})")
            item.setData(Qt.UserRole, result["pdf"])
            self.result_list.addItem(item)

        self.result_list.itemClicked.connect(self.open_link)

        
    def open_link(self, item):
        link = item.data(Qt.UserRole)
        if link:
            webbrowser.open(link)
        
    def create_history_Layout(self):
        history = self.user_data.get_search_history()
        main_widget = QWidget()
        main_layout = QHBoxLayout()

        terms_widget = QWidget()
        terms_layout = QVBoxLayout()
        terms_list = QListWidget()
        term_label = QLabel("searched terms")
        term_label.setAlignment(Qt.AlignHCenter)
        terms_layout.addWidget(term_label)
        terms_layout.addWidget(terms_list)
        terms_widget.setLayout(terms_layout)

        paper_widget = QWidget()
        paper_layout = QVBoxLayout()
        paper_list = QListWidget()
        paper_label = QLabel("viewed Paper")
        paper_label.setAlignment(Qt.AlignHCenter)
        paper_layout.addWidget(paper_label)
        paper_layout.addWidget(paper_list)
        paper_widget.setLayout(paper_layout)

        main_layout.addWidget(terms_widget)
        main_layout.addWidget(paper_widget)

        main_widget.setLayout(main_layout)

        return main_widget


    def create_settings_Layout(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        searchfield_widget = QWidget()
        searchfield_layout = QHBoxLayout()
        searchfield_label = QLabel("Scientific field:")
        self.searchfield_box = QComboBox()
        self.searchfield_box.addItems(["Accelerator Physics", "Physics"])

        searchfield_layout.addWidget(searchfield_label)
        searchfield_layout.addWidget(self.searchfield_box)
        searchfield_widget.setLayout(searchfield_layout)

        main_layout.addWidget(searchfield_widget)
        main_widget.setLayout(main_layout)

        return main_widget
