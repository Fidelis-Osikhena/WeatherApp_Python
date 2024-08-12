import os
import json
import requests
import tkinter as tk
from tkinter import messagebox
from tkinter import font
from weather_visualization import plot_temperature_trends
from dotenv import load_dotenv



# Load the .env file to get the API key
load_dotenv()
API_KEY = os.getenv('API_KEY')

FAVORITES_FILE = 'favorites.json'  # File to store favorite cities

# Function to get current weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather = {
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'description': data['weather'][0]['description'],
            'city': data['name'],
            'country': data['sys']['country']
        }
        return weather
    else:
        return None

# Function to search and display weather for a city
def search_weather():
    city = city_entry.get()
    if city:
        weather = get_weather(city)
        if weather:
            result_label.config(text=f"City: {weather['city']}, {weather['country']}\n"
                                     f"Temperature: {weather['temperature']}°C\n"
                                     f"Humidity: {weather['humidity']}%\n"
                                     f"Description: {weather['description']}")
        else:
            messagebox.showerror("Error", "City not found.")
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

# Function to load favorite cities from a file
def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r') as file:
            return json.load(file)
    return []

# Function to save favorite cities to a file
def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as file:
        json.dump(favorites, file)

# Function to add a city to favorites
def add_to_favorites():
    city = city_entry.get()
    if city:
        if city not in favorites:
            favorites.append(city)
            save_favorites(favorites)
            create_favorite_buttons()
            messagebox.showinfo("Success", f"{city} added to favorites.")
        else:
            messagebox.showwarning("Warning", f"{city} is already in favorites.")
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

# Function to delete a city from favorites
def delete_from_favorites(city):
    if city in favorites:
        favorites.remove(city)
        save_favorites(favorites)
        create_favorite_buttons()
        messagebox.showinfo("Success", f"{city} removed from favorites.")

# Function to create buttons for favorite cities
def create_favorite_buttons():
    for widget in favorites_frame.winfo_children():
        widget.destroy()
    for city in favorites:
        button_frame = tk.Frame(favorites_frame, bg="lightgrey")
        button_frame.pack(fill=tk.X, pady=2)

        city_button = tk.Button(button_frame, text=city, command=lambda c=city: quick_access_weather(c),
                                bg="lightblue", font=("Helvetica", 10, "bold"), relief="raised")
        city_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=lambda c=city: delete_from_favorites(c),
                                  bg="red", fg="white", font=("Helvetica", 10, "bold"), relief="raised")
        delete_button.pack(side=tk.LEFT, padx=5)

# Function to quickly access weather for a favorite city
def quick_access_weather(city):
    weather = get_weather(city)
    if weather:
        result_label.config(text=f"City: {weather['city']}, {weather['country']}\n"
                                 f"Temperature: {weather['temperature']}°C\n"
                                 f"Humidity: {weather['humidity']}%\n"
                                 f"Description: {weather['description']}")
    else:
        messagebox.showerror("Error", "City not found.")

# Function to show temperature trends using the imported function
def show_temperature_trends():
    city = city_entry.get()
    if city:
        plot_temperature_trends(city)
    else:
        messagebox.showwarning("Warning", "Please enter a city name.")

# Load favorites
favorites = load_favorites()

# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x500")
root.configure(bg="lightgrey")

# Fonts
title_font = tk.font.Font(family="Helvetica", size=16, weight="bold")
label_font = tk.font.Font(family="Helvetica", size=12)
button_font = tk.font.Font(family="Helvetica", size=10, weight="bold")

# Title Label
title_label = tk.Label(root, text="Weather App", font=title_font, bg="lightgrey")
title_label.pack(pady=10)

# Entry Frame for City Input
entry_frame = tk.Frame(root, bg="lightgrey")
entry_frame.pack(pady=10)

city_label = tk.Label(entry_frame, text="Enter city name:", font=label_font, bg="lightgrey")
city_label.pack(side=tk.LEFT, padx=5)

city_entry = tk.Entry(entry_frame, font=label_font)
city_entry.pack(side=tk.LEFT, padx=5)

# Search Weather Button
search_button = tk.Button(root, text="Search Weather", command=search_weather, bg="blue", fg="white",
                          font=button_font, relief="raised")
search_button.pack(pady=10)

# Add to Favorites Button
add_favorite_button = tk.Button(root, text="Add to Favorites", command=add_to_favorites, bg="green", fg="white",
                                font=button_font, relief="raised")
add_favorite_button.pack(pady=10)

# Show Temperature Trends Button
trend_button = tk.Button(root, text="Show Temperature Trends", command=show_temperature_trends, bg="orange", fg="white",
                         font=button_font, relief="raised")
trend_button.pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=label_font, bg="lightgrey", justify="left")
result_label.pack(pady=10)

# Favorites Label
favorites_label = tk.Label(root, text="Favorites:", font=label_font, bg="lightgrey")
favorites_label.pack(pady=10)

# Favorites Frame
favorites_frame = tk.Frame(root, bg="lightgrey")
favorites_frame.pack(pady=10)
create_favorite_buttons()

root.mainloop()