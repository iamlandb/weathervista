import requests
import pandas as pd
import sqlite3 as sql
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random

class Weather_Project:
    api_key = None
    location = None
    def __init__(self, api_key):
        self.api_key = api_key
        location = None
    def fetch_weather_data(api_key, location):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None
            
    def parse_weather_data(data):
        if data:
            weather = {
                "Location": data["name"],
                "Temperature (K)": data["main"]["temp"],
                "Humidity (%)": data["main"]["humidity"],
                "Weather": data["weather"][0]["description"]
            }
            return weather
        else:
            return None
            
    def save_to_csv(data, filename):
        df = pd.DataFrame([data])
        df.to_csv(filename, index=False)
        
    def fetch_data(url):
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            print("faild to fetch data")
            return None
        return data
        
    def parse_weather(entry):
        if entry is None:
            return None
        return {
            'Datetime': pd.to_datetime(entry['dt'], unit='s'),
            'Temperature (C)': entry['main']['temp'] - 273.15,
            'Humidity (%)': entry['main']['humidity'],
            'Wind Speed (m/s)': entry['wind']['speed'],
            'Weather': entry['weather'][0]['description']
        }
        
    def save_to_csv(data, filename):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"{filename} saved")
        
    def calculate_daily_stats(forecast_data):
        df_forecast = pd.DataFrame(forecast_data)
        df_forecast["Date"] = df_forecast["Datetime"].dt.date
        daily_stats =df_forecast.groupby("Date").agg({
            'Temperature (C)': ['min', 'max'],
            'Humidity (%)': ['min', 'max'],
            'Wind Speed (m/s)': ['min', 'max']
        })
        daily_stats.columns = ['Min Temperature (C)', 'Max Temperature (C)',
                                'Min Humidity (%)', 'Max Humidity (%)',
                                'Min Wind Speed (m/s)', 'Max Wind Speed (m/s)']
        daily_stats.reset_index(inplace = True)
        return daily_stats
        
        def convert_tempkelvin_to_celsius(temp_k):
            return_c = round(temp_k,2)
            return return_c
                