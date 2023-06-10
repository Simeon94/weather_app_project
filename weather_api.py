import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import requests
from tkinter import messagebox
from PIL import ImageTk, Image
import ttkbootstrap
import os

# Function to get weather for a city
class Weather_app:
    def __init__(self):
        self.API_key = os.environ.get('api_key')

        self.root = ttkbootstrap.Window(themename="morph")
        self.root.title("Weather App")
        self.root.geometry("400x400")

        #Scrollbar
        self.sf = ScrolledFrame(self.root, autohide=True)
        self.sf.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        # Entry widget -> to enter the city name
        self.city_entry = ttkbootstrap.Entry(self.sf, font="Helvetica, 18")
        self.city_entry.pack(pady=10)

        # Button widget -> to search for the weather information
        self.search_button = ttkbootstrap.Button(self.sf, text="Search", command=self.search, bootstyle="warning")
        self.search_button.pack(pady=10)

        # Label widget -> to show the city / country name
        self.location_label = tk.Label(self.sf,font="Helvetica, 25")
        self.location_label.pack()

        # Label widget -> to show the weather icon
        self.icon_label = tk.Label(self.sf)
        self.icon_label.pack()

        # Label widget -> to show the temperature
        self.temperature_label = tk.Label(self.sf, font="Helvetica, 20")
        self.temperature_label.pack()

        # Label widget -> to show the weather description
        self.description_label = tk.Label(self.sf, font="Helvetica, 20")
        self.description_label.pack()

    def get_weather(self, city):
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.API_key}"

        res = requests.get(url)
        
        if res.status_code != 404:
            # Parse the response JSON to get weather information
            weather = res.json()
            icon_id = weather["weather"][0]["icon"]
            temperature = weather["main"]["temp"] - 273.15
            description = weather["weather"][0]["description"]
            city = weather["name"]
            country = weather["sys"]["country"]
            print(weather)
        
            # Get the icon URL and return all the weather information
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            return (icon_url, temperature, description, city, country)
            
        else:
            messagebox.showerror("Error", "City not found, try again")
            return None
        
    # Function to search weather for a city
    def search(self):
        #self.city_entry= "Lagos"
        city = self.city_entry.get()
        result = self.get_weather(city)
        if result is None:
            return

        # If the city is found, unpack the weather information
        icon_url, temperature, description, city, country = result
        self.location_label.configure(text=f"{city}, {country}")
        
        # get the weather icon image from the URL and update the icon label
        try:
            image = Image.open(requests.get(icon_url, stream=True).raw) # exception handling
        except Exception as err:
            print(err)
            # placeholder url
            placeholder_url = "https://image.shutterstock.com/image-photo/adventure-on-mountain-bike-260nw-152465639.jpg"
            image = Image.open(requests.get(placeholder_url, stream=True).raw)
        
        icon = ImageTk.PhotoImage(image)
        self.icon_label.configure(image=icon)
        self.icon_label.image = icon

        # Update the temperature and description labels
        self.temperature_label.configure(text=f"Temperature: {temperature:.2f}degC")
        self.description_label.configure(text=f"Description: {description}")

    def run(self):
        self.root.mainloop()

weather_info = Weather_app()
weather_info.run()
