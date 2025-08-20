import requests
import os

from geopy.geocoders import Nominatim
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("WEATHER_API")
city = os.getenv("CITY")

geolocator = Nominatim(user_agent="smart-clock")

location = geolocator.geocode(city)

method = "current"

#https://api.weatherapi.com/v1/current.json?key=206761eff87144b19f0180126252008&q=Barcelona

base_uri = "https://api.weatherapi.com/v1"

raw_latitude, raw_longitude = location.latitude, location.longitude

lat = f"{raw_latitude:.3f}"
lon = f"{raw_longitude:.3f}"

print(raw_latitude, raw_longitude)

url = f"{base_uri}/{method}.json?key={api_key}&q={lat},{lon}"

print(url)
response = requests.get(url)

data = response.json()


current_condition = data["current"]["condition"]
current_ctemp = data["current"]["feelslike_c"]

condition_icon_uri = current_condition["icon"]
condition_text = current_condition["text"]

if "night" in condition_icon_uri:
    print("It's night time")
    night = True
elif "day" in condition_icon_uri:
    print("it's day time")
    day = True
else:
    print("It's neither")
    night = False
    day = False

print(condition_icon_uri)