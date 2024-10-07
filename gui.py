from PyQt5 import QtWidgets
import sys
import requests
import sqlite3

class WeatherApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Weather App')

        self.layout = QtWidgets.QVBoxLayout()

        self.city_input = QtWidgets.QLineEdit(self)
        self.layout.addWidget(self.city_input)

        self.button = QtWidgets.QPushButton('Get Weather', self)
        self.button.clicked.connect(self.get_weather)
        self.layout.addWidget(self.button)

        self.weather_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.weather_label)

        self.setLayout(self.layout)

    def get_weather(self):
        city = self.city_input.text()  # Get the city from the input field
        conn = sqlite3.connect('weather_data.db')  # Connect to your SQLite database
        cursor = conn.cursor()
        
        # Query to fetch weather data for the specified city
        cursor.execute('''
            SELECT date, time, temp, dew_point, relative_humidity, wind_dir, wind_speed, gust_wind_speed, ncpcp, cncpcp, snowfall 
            FROM weather_conditions WHERE location = ?
        ''', (city,))
        
        weather_data = cursor.fetchall()  # Fetch all matching rows

        # Check if any data was found
        if weather_data:
            # Format the output for the label
            weather_info = ""
            for row in weather_data:
                weather_info += f"Date: {row[0]}, Time: {row[1]}, Temperature: {row[2]} °F, Dew Point: {row[3]} °F, "
                weather_info += f"Relative Humidity: {row[4]}%, Wind Direction: {row[5]}, Wind Speed: {row[6]} mi/h, "
                weather_info += f"Gust Wind Speed: {row[7]} mi/h, NCPCP: {row[8]}, CNCPCP: {row[9]}, Snowfall: {row[10]} in"
            
            self.weather_label.setText(weather_info)  # Update label with the weather info
        else:
            self.weather_label.setText("City not found in the database.")
        
        # Close the database connection
        conn.close()

app = QtWidgets.QApplication(sys.argv)
window = WeatherApp()
window.show()
sys.exit(app.exec_())