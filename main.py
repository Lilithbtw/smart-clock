# Backend Libs
import sys
import os

# Frontend Libs
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFontDatabase, QFont

# weather.py import
from weather import WeatherMonitor

class SmartClock(QWidget):
    def __init__(self):
        super().__init__()
        # Initialize QLabels and run initUi
        self.time_label = QLabel(self)
        self.ctemp = QLabel(self)
        self.weather = QLabel(self)
        self.timer = QTimer(self)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart Clock")
        self.showMaximized()

        vbox = QVBoxLayout()

        # Clock in center
        self.time_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.time_label, alignment=Qt.AlignCenter)

        self.ctemp.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.ctemp, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        self.setLayout(vbox)

        # Font loading
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "JetBrainsMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 150)
            font_small = QFont(font_family, 25)
        else:
            print("Failed to load JetBrains Mono. Using fallback font.")
            font = QFont("Sans Serif", 150)
            font_small = QFont("Sans Serif", 25)
        # Font loading Time Label
        self.time_label.setFont(font)

        # Font loading ctemp and weather
        self.ctemp.setFont(font_small)

        # Styling
        self.setStyleSheet("background-color: black")
        self.time_label.setStyleSheet("color: white")
        
        self.ctemp.setStyleSheet("color: white")

        # Timer
        self.timer.timeout.connect(self.UpdateTime)
        self.timer.start(1*1000)
        self.UpdateTime()

        # Weather and ctemp
        self.timer.timeout.connect(self.CheckWeather)
        self.timer.start(1*1000)
        self.CheckWeather()

    def UpdateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

    def CheckWeather(self):
        monitor = WeatherMonitor()
        monitor.update_weather()
        self.ctemp.setText(monitor.ctemp)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = SmartClock()
    clock.show()
    sys.exit(app.exec_())
