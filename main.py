#* Backend Libs*
import sys
import os
from datetime import date, datetime
import json
#* Frontend Libs*
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy, QSpacerItem
from PyQt5.QtCore import Qt, QTimer, QTime
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtSvg import QSvgWidget
#* weather.py import*
from weather import WeatherMonitor

class SmartClock(QWidget):
    def __init__(self):
        super().__init__()

        # Initialize Qlabels
        self.time_label = QLabel(self)
        self.ctemp = QLabel(self)
        self.weather = QLabel(self)
        self.weather_condition = QLabel(self)
        self.day = QLabel(self)

        # Weather Icon - Reduced size for better visual balance
        self.weather_icon = QSvgWidget(self)
        self.weather_icon.setFixedSize(80, 68)  # More proportional size
        
        try:
            self.weather_monitor = WeatherMonitor()
            print("WeatherMonitor correctly initialized")
        except Exception as e:
            print(f"Error initializing WeatherMonitor: {e}")
            self.weather_monitor = None
        
        self.time_timer = QTimer(self)
        self.weather_timer = QTimer(self)
        
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Smart Clock")
        self.showMaximized()
        
        vbox = QVBoxLayout()

        # Add top spacer for proper vertical positioning
        vbox.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # Create weather widget container for centered grouping
        weather_container = QWidget()
        weather_layout = QHBoxLayout(weather_container)
        weather_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        weather_layout.setSpacing(12)  # Optimal spacing between icon and temp

        # Weather icon with proper sizing policy
        self.weather_icon.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        weather_layout.addWidget(self.weather_icon)

        # Temperature with baseline alignment
        self.ctemp.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        weather_layout.addWidget(self.ctemp)

        # Center the entire weather container
        weather_container_layout = QHBoxLayout()
        weather_container_layout.addStretch()
        weather_container_layout.addWidget(weather_container)
        weather_container_layout.addStretch()
        
        vbox.addLayout(weather_container_layout)

        # Spacer with proper proportional expansion
        vbox.addSpacerItem(QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Clock in the Center - Main focal point
        self.time_label.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.time_label, alignment=Qt.AlignCenter)

        # Weather condition text - Secondary information
        self.weather_condition.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.weather_condition, alignment=Qt.AlignCenter)

        # Spacer for bottom section
        vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Day - Bottom aligned with proper spacing
        self.day.setAlignment(Qt.AlignCenter)
        vbox.addWidget(self.day, alignment=Qt.AlignBottom | Qt.AlignHCenter)
        
        # Add bottom margin
        vbox.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))
        
        self.setLayout(vbox)
        
        # Font loading with improved hierarchy
        font_path = os.path.join(os.path.dirname(__file__), "fonts", "JetBrainsMono-Regular.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font_clock = QFont(font_family, 150)
            font_temp = QFont(font_family, 28)      # Larger for better readability
            font_small = QFont(font_family, 20)
            font_medium = QFont(font_family, 25)
        else:
            print("Failed to load JetBrains Mono. Using fallback font.")
            font_clock = QFont("Sans Serif", 150)
            font_temp = QFont("Sans Serif", 28)
            font_small = QFont("Sans Serif", 20)
            font_medium = QFont("Sans Serif", 25)
            
        self.time_label.setFont(font_clock)
        self.ctemp.setFont(font_temp)
        self.day.setFont(font_small)
        self.weather_condition.setFont(font_medium)
        
        # Enhanced styling with better visual hierarchy
        self.setStyleSheet("background-color: black")
        self.time_label.setStyleSheet("color: white; font-weight: 300;")  # Lighter weight for elegance
        self.ctemp.setStyleSheet("color: white; font-weight: 400;")       # Medium weight for readability
        self.day.setStyleSheet("color: #CCCCCC;")                         # Slightly lighter for hierarchy
        self.weather_condition.setStyleSheet("color: #888888; font-weight: 300;")  # Subtle secondary text
        
        # Timer para reloj (cada segundo)
        self.time_timer.timeout.connect(self.UpdateTime)
        self.time_timer.timeout.connect(self.UpdateDay)
        self.time_timer.start(1000)
        
        # Timer para clima (cada 10 minutos = 600000 ms)
        self.weather_timer.timeout.connect(self.CheckWeather)
        self.weather_timer.start(600000)  # 10 minutos
        
        # Inicializar valores
        self.UpdateTime()
        self.UpdateDay()
        self.CheckWeather()  # Primera actualización del clima

    def UpdateTime(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(current_time)

    def load_svg(self, code: str, is_day: bool):
        """Load SVG based on weather code and day/night flag"""
        try:
            mapping = os.path.join(os.path.dirname(__file__), "icons", "weather-mapping.json")
            with open(mapping, 'r') as file:
                data = json.load(file)
            
            if code in data:
                key = "day" if is_day else "night"
                icon_file = data[code][key]["icon"]
                icon_path = os.path.join(os.path.dirname(__file__), "icons", icon_file)
                if os.path.exists(icon_path):
                    self.weather_icon.load(icon_path)
                else:
                    print(f"Icon not found: {icon_path}")
        except Exception as e:
            print(f"Error loading icon: {e}")

    def CheckWeather(self):
        try:
            if not self.weather_monitor:
                print("WeatherMonitor is not initialized")
                self.ctemp.setText("Error Init")
                return
            
            success = self.weather_monitor.update_weather()
            # Temp
            if hasattr(self.weather_monitor, 'ctemp') and self.weather_monitor.ctemp:
                self.ctemp.setText(self.weather_monitor.ctemp)
            else:
                self.ctemp.setText("--°C")
            
            # Condition Text
            if hasattr(self.weather_monitor, "condition_text") and self.weather_monitor.condition_text:
                self.weather_condition.setText(self.weather_monitor.condition_text)
            else:
                self.weather_condition.setText("")

            # Icon
            if hasattr(self.weather_monitor, "condition_code"):
                code = str(self.weather_monitor.condition_code)
                is_day = self.weather_monitor.is_daytime()
                self.load_svg(code, is_day)

            if success:
                print(f"Clima actualizado: {self.weather_monitor.ctemp}")
                
        except AttributeError as e:
            print(f"Atribute Error: {e}")
            print("Verify that weather_monitor is correctly initialized")
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