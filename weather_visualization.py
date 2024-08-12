import requests
import matplotlib.pyplot as plt
import datetime
from tkinter import messagebox
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv('API_KEY')  

def get_location_coordinates(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['coord']['lat'], data['coord']['lon']
    else:
        return None, None

def get_historical_weather(lat, lon, dt):
    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}&dt={dt}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def plot_temperature_trends(city):
    lat, lon = get_location_coordinates(city)
    if lat is None or lon is None:
        messagebox.showerror("Error", "Could not find location.")
        return
    
    dates = []
    temperatures = []

    for days_back in range(7):
        dt = datetime.datetime.now() - datetime.timedelta(days=days_back)
        dt_timestamp = int(dt.timestamp())
        weather_data = get_historical_weather(lat, lon, dt_timestamp)

        if weather_data:
            dates.append(dt.strftime("%Y-%m-%d"))
            temperatures.append(weather_data['current']['temp'])
    
    dates.reverse()
    temperatures.reverse()

    plt.figure(figsize=(10, 5))
    plt.plot(dates, temperatures, marker='o')
    plt.title(f"Temperature Trends for {city}")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.grid(True)
    plt.show()
