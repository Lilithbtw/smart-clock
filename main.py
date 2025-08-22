#* Backend Libs*
import sys
import os
from datetime import date, datetime
#* Frontend Libs*
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFontDatabase, QFont
#* weather.py import*
from weather import WeatherMonitor

class SmartClock(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Qlabels
        self.time_label = QLabel(self)
        self.ctemp = QLabel(self)
        self.weather = QLabel(self)
        self.day = QLabel(self)
        
        try:
            self.weather_monitor = WeatherMonitor()
            print("WeatherMonitor inicializado correctamente")
        except Exception as e:
            print(f"Error inicializando WeatherMonitor: {e}")
            self.weather_monitor = None
        
        self.time_timer = QTimer(self)
        self.weather_timer = QTimer(self)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart Clock")
        self.showMaximized()
        
        vbox = QVBoxLayout()
        
        # Temperature
        self.ctemp.setAlignment(Qt.AlignRight | Qt.AlignTop)
        vbox.addWidget(self.ctemp, alignment=Qt.AlignRight | Qt.AlignTop)
        
        # Clock in the Center
        self.time_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.time_label, alignment=Qt.AlignCenter)
        
        # Day
        self.day.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.day, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        
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
        
        self.time_label.setFont(font)
        self.ctemp.setFont(font_small)
        self.day.setFont(font_small)
        
        # Styling
        self.setStyleSheet("background-color: black")
        self.time_label.setStyleSheet("color: white")
        self.ctemp.setStyleSheet("color: white")
        self.day.setStyleSheet("color: white")
        
        # Timer para reloj (cada segundo)
        self.time_timer.timeout.connect(self.UpdateTime)
        self.time_timer.timeout.connect(self.UpdateDay)
        self.time_timer.start(1000)
        
        # Timer para clima (cada 10 minutos = 600000 ms)
        self.weather_timer.timeout.connect(self.CheckWeather)
        self.weather_timer.start(600000)  # 10 minutos
        
        #* Inicializar valores*
        self.UpdateTime()
        self.UpdateDay()
        self.CheckWeather()  # Primera actualización del clima

    def UpdateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

    def CheckWeather(self):
        try:
            # Verificar que weather_monitor existe
            if not self.weather_monitor:
                print("WeatherMonitor no está inicializado")
                self.ctemp.setText("Error Init")
                return
            
            # Llamar update_weather() del weather_monitor
            success = self.weather_monitor.update_weather()
            
            # Actualizar la UI con el valor actual (exitoso o no)
            if hasattr(self.weather_monitor, 'ctemp') and self.weather_monitor.ctemp:
                self.ctemp.setText(self.weather_monitor.ctemp)
            else:
                self.ctemp.setText("--°C")
                
            if success:
                print(f"Clima actualizado: {self.weather_monitor.ctemp}")
                
        except AttributeError as e:
            print(f"Error de atributo: {e}")
            print("Verificar que weather_monitor esté inicializado correctamente")
            self.ctemp.setText("Error Attr")
        except Exception as e:
            print(f"Error updating weather display: {e}")
            self.ctemp.setText("--°C")

    def UpdateDay(self):
        dias_de_la_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        hoy = datetime.now()
        dia = hoy.weekday()
        self.day.setText(dias_de_la_semana[dia])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = SmartClock()
    clock.show()
    sys.exit(app.exec_())