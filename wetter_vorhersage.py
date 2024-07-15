import requests
import json
import random
from geopy.geocoders import Nominatim

# Funktion zum Laden der Aktivitäten aus der JSON-Datei
def load_activities(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Funktion zum Laden der Wettercodes aus der JSON-Datei
def load_weather_codes(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

# Aktivitäten und Wettercodes laden
activities = load_activities('activities.json')
weather_codes = load_weather_codes('weather_codes.json')

# Funktion zum Abrufen der Wetterdaten von Open-Meteo
def get_weather_data(latitude, longitude):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,weathercode&timezone=Europe/Berlin"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Funktion zum Übersetzen des Wettercodes in Klartext
def translate_weather_code(code):
    return weather_codes.get(str(code), "Unbekannt")

# Funktion zur Empfehlung von Aktivitäten basierend auf dem Wettercode
def recommend_activities(code):
    if code in [0, 1, 2, 3]:  # Gutes Wetter
        selected_activities = random.sample(activities['outdoor'], 4)
        recommendation = "Outdoor-Aktivitäten empfohlen:\n" + "\n".join(
            f"- {activity}" for activity in selected_activities)
    elif code in [45, 48, 51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99]:  # Schlechtes Wetter
        selected_activities = random.sample(activities['indoor'], 4)
        recommendation = "Indoor-Aktivitäten empfohlen:\n" + "\n".join(
            f"- {activity}" for activity in selected_activities)
    elif code in [71, 73, 75, 77, 85, 86]:  # Schneewetter
        selected_activities = random.sample(activities['snow'], 4)
        recommendation = "Outdoor-Aktivitäten empfohlen (warme Kleidung nötig):\n" + "\n".join(
            f"- {activity}" for activity in selected_activities)
    else:
        recommendation = "Aktivitäten je nach Wetterlage anpassen"
    return recommendation

# Funktion zum Abrufen und Formatieren der Wetterdaten
def get_formatted_weather(latitude, longitude):
    data = get_weather_data(latitude, longitude)
    if data:
        today = data['daily']['time'][0]
        tomorrow = data['daily']['time'][1]
        day_after_tomorrow = data['daily']['time'][2]

        temp_today_max = data['daily']['temperature_2m_max'][0]
        temp_today_min = data['daily']['temperature_2m_min'][0]
        weather_code_today = data['daily']['weathercode'][0]

        temp_tomorrow_max = data['daily']['temperature_2m_max'][1]
        temp_tomorrow_min = data['daily']['temperature_2m_min'][1]
        weather_code_tomorrow = data['daily']['weathercode'][1]

        temp_day_after_tomorrow_max = data['daily']['temperature_2m_max'][2]
        temp_day_after_tomorrow_min = data['daily']['temperature_2m_min'][2]
        weather_code_day_after_tomorrow = data['daily']['weathercode'][2]

        weather_info = {
            "today": {
                "date": today,
                "max_temp": temp_today_max,
                "min_temp": temp_today_min,
                "weather": translate_weather_code(weather_code_today),
                "recommendation": recommend_activities(weather_code_today)
            },
            "tomorrow": {
                "date": tomorrow,
                "max_temp": temp_tomorrow_max,
                "min_temp": temp_tomorrow_min,
                "weather": translate_weather_code(weather_code_tomorrow),
                "recommendation": recommend_activities(weather_code_tomorrow)
            },
            "day_after_tomorrow": {
                "date": day_after_tomorrow,
                "max_temp": temp_day_after_tomorrow_max,
                "min_temp": temp_day_after_tomorrow_min,
                "weather": translate_weather_code(weather_code_day_after_tomorrow),
                "recommendation": recommend_activities(weather_code_day_after_tomorrow)
            }
        }
        return weather_info
    else:
        return None

# Funktion zum Abrufen der Koordinaten einer Stadt
def get_coordinates(city_name):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(city_name)
    if location:
        return location.latitude, location.longitude
    return None, None

if __name__ == "__main__":
    latitude, longitude = get_coordinates("Berlin")
    weather_info = get_formatted_weather(latitude, longitude)
    if weather_info:
        for day, info in weather_info.items():
            print(f"Datum: {info['date']}")
            print(f"Max: {info['max_temp']}°C, Min: {info['min_temp']}°C")
            print(f"Wetter: {info['weather']}")
            print(f"Empfehlung: {info['recommendation']}\n")
    else:
        print("Fehler beim Laden der Wetterdaten")