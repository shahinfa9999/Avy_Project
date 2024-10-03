#import Avalanche_Conditions as AC
import os
import pandas as pd

import sqlite3

# Create a connection to SQLite database
conn = sqlite3.connect('weather_data.db')
cursor = conn.cursor()

# Create the table to store the data
cursor.execute('''
CREATE TABLE IF NOT EXISTS weather_conditions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location TEXT,
    latitude TEXT,
    longitude TEXT,
    date TEXT,
    time TEXT,
    temp TEXT,
    dew_point TEXT,
    relative_humidity TEXT,
    wind_dir TEXT,
    wind_speed TEXT,
    gust_wind_speed TEXT,
    ncpcp TEXT,
    cncpcp TEXT,
    snowfall TEXT
)
''')

# Read the file
for filename in os.listdir('downloaded_txt_files'):
    with open(os.path.join('downloaded_txt_files', filename)) as file:
        for line in file:
            if "LOCATION" in line:
                location = line.split(":")[1].strip().split(" ")[0]
                Latitude = line.split(":")[2].strip().split(" ")[0]
                Longitude = line.split(":")[3].strip().split(" ")[0]
            if "CLEAR" in line: #this needs to be update to include not just clear but all the other conditions
                date = line.split("/")[0].strip().split(" ")[0]+"/"+line.split("/")[1].strip().split(" ")[0]+"/"+line.split("/")[2].strip().split(" ")[0]
                time = line.split(" ")[1].strip()
                temp = line.split(" ")[3].strip()
                dew_point = line.split(" ")[5].strip()
                relative_humidity = line.split(" ")[7].strip()
                wind_dir = line.split(" ")[8].strip().split("/")[0]
                wind_speed = line.split("/")[3].strip()
                gust_wind_speed = line.split(" ")[11].strip()
                #Non_Convective_Precipitation
                ncpcp = line.split(" ")[19]
                #print(ncpcp)
                #convective_precipitation
                cncpcp = line.split(" ")[21]
                #print(cncpcp)
                #snowfall
                snowfall = line.split(" ")[23]
                #print(snowfall)
                # Insert the data into the table

                 # Insert data into the table
                cursor.execute('''
                    INSERT INTO weather_conditions (
                        location, latitude, longitude, date, time, temp, dew_point,
                        relative_humidity, wind_dir, wind_speed, gust_wind_speed,
                        ncpcp, cncpcp, snowfall
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (location, Latitude, Longitude, date, time, temp, dew_point,
                      relative_humidity, wind_dir, wind_speed, gust_wind_speed, ncpcp, cncpcp, snowfall))

                #print(f"Temperature: {temp}", f"Dew Point: {dew_point}", f"Relative Humidity: {relative_humidity}", f"Wind Direction: {wind_dir}", f"Wind Speed: {wind_speed}")
conn.commit()
conn.close()

print("Data has been saved to the database")

# Function to fetch data for a specific location
# Function to fetch data for a specific location
def get_data_by_location(location):
    # Create a new connection to fetch the data
    conn = sqlite3.connect('weather_data.db')
    cursor = conn.cursor()
    
    # Execute the SELECT query
    cursor.execute('''
        SELECT * FROM weather_conditions WHERE location = ?
    ''', (location,))
    
    # Fetch all matching rows
    rows = cursor.fetchall()

    # Check if any data was found
    if rows:
        for row in rows:
            print(row)  # Format the output as needed
    else:
        print(f"No data found for location: {location}")
    
    # Close the connection after querying
    conn.close()

# Example: Get data for a specific location, e.g., 'Denver'
get_data_by_location('DENVER')