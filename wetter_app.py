import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QLineEdit
from wetter_vorhersage import get_formatted_weather, get_coordinates

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wettervorhersage")

        self.weather_info = None
        self.setFixedSize(QSize(500, 800))

        self.create_widgets()

    def create_widgets(self):
        self.layout = QVBoxLayout()

        self.input_label = QLabel("Geben Sie eine Stadt oder einen Ort für die Wetterabfrage ein:", self)
        self.layout.addWidget(self.input_label)

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Geben Sie eine Stadt ein")
        self.layout.addWidget(self.city_input)

        self.search_button = QPushButton("Suche", self)
        self.search_button.clicked.connect(self.update_weather)
        self.layout.addWidget(self.search_button)

        self.today_label = QLabel("", self)
        self.layout.addWidget(self.today_label)

        self.tomorrow_label = QLabel("", self)
        self.layout.addWidget(self.tomorrow_label)

        self.day_after_tomorrow_label = QLabel("", self)
        self.layout.addWidget(self.day_after_tomorrow_label)

        self.setLayout(self.layout)

    def update_weather(self):
        city_name = self.city_input.text()
        latitude, longitude = get_coordinates(city_name)
        if latitude and longitude:
            self.weather_info = get_formatted_weather(latitude, longitude)
            if self.weather_info:
                self.today_label.setText(self.format_weather_info("Heute", self.weather_info["today"]))
                self.tomorrow_label.setText(self.format_weather_info("Morgen", self.weather_info["tomorrow"]))
                self.day_after_tomorrow_label.setText(
                    self.format_weather_info("Übermorgen", self.weather_info["day_after_tomorrow"]))
            else:
                self.today_label.setText("Fehler beim Laden der Wetterdaten")
                self.tomorrow_label.setText("")
                self.day_after_tomorrow_label.setText("")
        else:
            self.today_label.setText("Stadt nicht gefunden")
            self.tomorrow_label.setText("")
            self.day_after_tomorrow_label.setText("")

    def format_weather_info(self, day_name, info):
        return (
            f"{day_name} ({info['date']}):\n"
            f"Max: {info['max_temp']}°C, Min: {info['min_temp']}°C\n"
            f"Wetter: {info['weather']}\n"
            f"Empfehlung: {info['recommendation']}"
        )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())