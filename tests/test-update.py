from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtCore import Qt, QTimer

class GrowingCircle(QWidget):
    def __init__(self):
        super().__init__()
        self.radius = 10
        self.growing = True

        # Timer to change state every 100ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.change_state)
        self.timer.start(100)

        self.setWindowTitle("Circle with update()")
        self.resize(300, 300)

    def change_state(self):
        # Grow/shrink the circle
        if self.growing:
            self.radius += 5
            if self.radius >= 100:
                self.growing = False
        else:
            self.radius -= 5
            if self.radius <= 10:
                self.growing = True

        self.update()  # request a repaint (calls paintEvent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(Qt.blue))

        # Draw circle centered in widget
        center_x = self.width() // 2
        center_y = self.height() // 2
        painter.drawEllipse(center_x - self.radius,
                            center_y - self.radius,
                            2 * self.radius,
                            2 * self.radius)

app = QApplication([])
w = GrowingCircle()
w.show()
app.exec_()
