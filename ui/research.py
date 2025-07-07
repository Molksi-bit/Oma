from PySide6.QtWidgets import (
    QMainWindow, QWidget,QHBoxLayout,QVBoxLayout,QTableWidget,QTableWidgetItem,QMenuBar,QMenu,QFrame,QStackedWidget, QSizePolicy, QFileDialog,QLabel,QListWidget, QListWidgetItem,QMessageBox,
    QPushButton,QApplication,QScrollArea, QLineEdit, QScrollBar,QStyle)
import os
from PySide6.QtCore import Qt
import webbrowser
import requests
import feedparser

class ResearchWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Research")
        self.setMinimumSize(600,400)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)
        self.views = {
            "home" : self.create_home_layout()
        }
        for view in self.views.values():
            self.stacked.addWidget(view)
        self.create_menu()

    def create_menu(self):
        pass

    def create_home_layout(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        searchfield = QWidget()
        searchfield_layout = QHBoxLayout()

        self.label = QLabel("Keywords:")
        searchfield_layout.addWidget(self.label)

        self.entry_field = QLineEdit()
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
        self.result_list.clear()
        if not entry:
            return
        
        clean_entry = entry.replace(" ","+")
        url = f"http://export.arxiv.org/api/query?search_query=all:{clean_entry}+AND+cat:physics.acc-ph&start=0&max_results=10"

        response = requests.get(url)
        if response.status_code != 200:
            print(f"Fehler: HTTP {response.status_code}")
            return []
        feed = feedparser.parse(response.text)
        results = []
        for entry in feed.entries:
            results.append({
                "title": entry.title,
                "published": entry.published,
                "link": entry.link
            })
        for result in results:
            item = QListWidgetItem(f"{result['title']} ({result['published']})")
            item.setData(Qt.UserRole, result["link"])
            self.result_list.addItem(item)

        self.result_list.itemClicked.connect(self.open_link)

        
    def open_link(self, item):
        link = item.data(Qt.UserRole)
        if link:
            webbrowser.open(link)
