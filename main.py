import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSpacerItem, QSizePolicy
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

        self.label_2 = QLabel('This is the second label', self)
        self.label_2.setStyleSheet("color: blue;"
                                   "border: 3px solid green")


        self.label_3 = QLabel('This is the third label', self)
        self.label_3.setStyleSheet("color: blue;"
                                   "border: 3px solid green")


        vbox.addWidget(self.label_2)

        vbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        vbox.addWidget(self.time_label, alignment=Qt.AlignCenter)
        vbox.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(vbox)

        self.time_label.setAlignment(Qt.AlignCenter)

        font_path = os.path.join(os.path.dirname(__file__), "fonts", "JetBrainsMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)

        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(font_family, 150)
        else:
            print("Failed to load JetBrains Mono. Using fallback font.")
            font = QFont("Sans Serif", 150)
            
        self.time_label.setFont(font)
        self.setStyleSheet("background-color: black")
        self.time_label.setStyleSheet("color: white")
        
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