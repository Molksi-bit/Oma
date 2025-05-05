from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt, QTimer


class showVideo(QWidget):

    def __init__(self,video,callback,duration = 3000):
        """This function starts the opening gif of the Programm."""
        super().__init__()
        self.setObjectName("gif")
        self.setWindowFlags(Qt.FramelessWindowHint| Qt.SplashScreen)
        self.setFixedSize(500,500)

        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(True)
        self.movie = QMovie(video)
        self.movie.setScaledSize(self.size())
        self.label.setMovie(self.movie)
        self.label.setObjectName("giflabel")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)
        self.movie.start()
        QTimer.singleShot(duration,self.finish)
        self.callback = callback

    def finish(self):
        """This function finishes the gif and closes the window."""
        self.movie.stop()
        self.callback()
        self.close()
