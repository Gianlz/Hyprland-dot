#!/usr/bin/env python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': '☀️ ',
    '116': '⛅ ',
    '119': '☁️ ',
    '122': '☁️ ',
    '143': '☁️ ',
    '176': '🌧️',
    '179': '🌧️',
    '182': '🌧️',
    '185': '🌧️',
    '200': '⛈️ ',
    '227': '🌨️',
    '230': '🌨️',
    '248': '☁️ ',
    '260': '☁️ ',
    '263': '🌧️',
    '266': '🌧️',
    '281': '🌧️',
    '284': '🌧️',
    '293': '🌧️',
    '296': '🌧️',
    '299': '🌧️',
    '302': '🌧️',
    '305': '🌧️',
    '308': '🌧️',
    '311': '🌧️',
    '314': '🌧️',
    '317': '🌧️',
    '320': '🌨️',
    '323': '🌨️',
    '326': '🌨️',
    '329': '❄️ ',
    '332': '❄️ ',
    '335': '❄️ ',
    '338': '❄️ ',
    '350': '🌧️',
    '353': '🌧️',
    '356': '🌧️',
    '359': '🌧️',
    '362': '🌧️',
    '365': '🌧️',
    '368': '🌧️',
    '371': '❄️',
    '374': '🌨️',
    '377': '🌨️',
    '386': '🌨️',
    '389': '🌨️',
    '392': '🌧️',
    '395': '❄️ '
}

data = {}

weather = requests.get("https://wttr.in/?format=j1").json()

def format_time(time):
    return time.replace("00", "").zfill(2)

def fahrenheit_to_celsius(fahrenheit):
    return round((float(fahrenheit) - 32) * 5/9, 1)

def format_temp(temp_f):
    temp_c = fahrenheit_to_celsius(temp_f)
    return f"{temp_c}°C"

def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(f"{chances[event]} {hour[event]}%")
    return ", ".join(conditions)

temp_f = float(weather['current_condition'][0]['FeelsLikeF'])
temp_c = fahrenheit_to_celsius(temp_f)
extrachar = '+' if temp_c > 0 else ''

data['text'] = ' ' + WEATHER_CODES[weather['current_condition'][0]['weatherCode']] + \
    f" {extrachar}{temp_c}°C"

data['tooltip'] = f"<b>{weather['current_condition'][0]['weatherDesc'][0]['value']} {weather['current_condition'][0]['temp_F']}°F</b>\n"
data['tooltip'] += f"Feels like: {temp_f}°F / {temp_c}°C\n"
data['tooltip'] += f"Wind: {weather['current_condition'][0]['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {weather['current_condition'][0]['humidity']}%\n"
for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f"⬆️ {day['maxtempF']}°F / {fahrenheit_to_celsius(day['maxtempF'])}°C ⬇️ {day['mintempF']}°F / {fahrenheit_to_celsius(day['mintempF'])}°C "
    data['tooltip'] += f"🌅 {day['astronomy'][0]['sunrise']} 🌇 {day['astronomy'][0]['sunset']}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])} {WEATHER_CODES[hour['weatherCode']]} {format_temp(hour['FeelsLikeF'])} {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"

print(json.dumps(data))
