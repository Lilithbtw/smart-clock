# Backend Libs
import sys
import os
import requests

# Frontend Libs
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFontDatabase, QFont

class SmartClock(QWidget):
    def __init__(self):
        super().__init__()
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart Clock")
        self.showMaximized()

        vbox = QVBoxLayout()

        # Clock in center
        self.time_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.time_label, alignment=Qt.AlignCenter)

        self.setLayout(vbox)

        # Font loading
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "JetBrainsMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 150)
        else:
            print("Failed to load JetBrains Mono. Using fallback font.")
            font = QFont("Sans Serif", 150)

        self.time_label.setFont(font)

        # Styling
        self.setStyleSheet("background-color: black")
        self.time_label.setStyleSheet("color: white")

        # Timer
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1000)
        self.UpdateTime()

    def UpdateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = SmartClock()
    clock.show()
    sys.exit(app.exec_())
