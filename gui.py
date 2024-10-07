from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys
import sqlite3
import pandas as pd

class DataViewer(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('City Data Viewer')
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        layout = QVBoxLayout()

        # City input field
        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText('Enter City Name')
        layout.addWidget(self.city_input)

        # Fetch data button
        self.fetch_button = QPushButton('Fetch Data', self)
        self.fetch_button.clicked.connect(self.fetch_data)
        layout.addWidget(self.fetch_button)

        # Table for displaying fetched data
        self.table_widget = QTableWidget(self)
        layout.addWidget(self.table_widget)

        # Matplotlib canvas for displaying plots
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def fetch_data(self):
        city = self.city_input.text()
        if not city:
            QMessageBox.warning(self, 'Input Error', 'Please enter a city name')
            return

        # Connect to the SQLite database and fetch data for the specified city
        conn = sqlite3.connect('weather_data.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM weather_conditions WHERE location = ?', (city,))
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            QMessageBox.information(self, 'No Data', 'No data found for the specified city')
            return

        # Populate the table widget with data
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0]))
        self.table_widget.setHorizontalHeaderLabels([
            'ID', 'Location', 'Latitude', 'Longitude', 'Date', 'Time', 'Temp', 
            'Dew Point', 'Relative Humidity', 'Wind Dir', 'Wind Speed', 
            'Gust Wind Speed', 'NCPCP', 'CNCPCP', 'Snowfall'
        ])

        for row_idx, row_data in enumerate(rows):
            for col_idx, col_data in enumerate(row_data):
                self.table_widget.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        # Extract data for plotting
        self.plot_data(city)

    def plot_data(self, city):
        # Fetch the weather data from the database for the specified city
        conn = sqlite3.connect('weather_data.db')
        query = '''
        SELECT date, time, temp, dew_point, relative_humidity
        FROM weather_conditions
        WHERE location = ?
        '''
        df = pd.read_sql_query(query, conn, params=(city,))
        conn.close()

        if df.empty:
            QMessageBox.information(self, 'No Data', 'No weather data available to plot')
            return

        # Convert date and time to a datetime object for plotting
        df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'])

        # Clear any existing plots in the figure
        self.figure.clear()

        # Create an axis for the new plot
        ax = self.figure.add_subplot(111)

        # Plot the temperature and dew point
        ax.plot(df['datetime'], df['temp'], label='Temperature (°F)', color='orange')
        ax.plot(df['datetime'], df['dew_point'], label='Dew Point (°F)', color='blue')
        ax.fill_between(df['datetime'], df['temp'], df['dew_point'], color='lightblue', alpha=0.5)

        # Set labels, title, and legend
        ax.set_title(f"Weather Conditions for {city}")
        ax.set_xlabel('Date and Time')
        ax.set_ylabel('Temperature (°F) & Dew Point (°F)')
        ax.legend()
        ax.grid()

        # Refresh the canvas to display the updated plot
        self.canvas.draw()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    viewer = DataViewer()
    viewer.show()
    sys.exit(app.exec_())