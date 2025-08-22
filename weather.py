import requests
import os
import time

from geopy.geocoders import Nominatim
from dotenv import load_dotenv

def loadConfig():
    env_vars = ["WEATHER_API", "CITY", "UPDATE_INTERVAL"]

    for var in env_vars:
        if var in os.environ:
            del os.environ[var]

    # Load Values
    load_dotenv(override=True)
    
    api_key = os.getenv("WEATHER_API")
    city = os.getenv("CITY")
    update_interval = float(os.getenv("UPDATE_INTERVAL"))

    return api_key, city, update_interval


def GetLocation(city):
    geolocator = Nominatim(user_agent="smart-clock")
    location = geolocator.geocode(city)

    lat = f"{location.latitude:.3f}"
    lon = f"{location.longitude:.3f}"
    
    return lat, lon

def fetchData(api_key, city):
    """Fetch current Weather for the city"""
    try:
        method = "current"
        base_uri = "https://api.weatherapi.com/v1"
        url = f"{base_uri}/{method}.json?key={api_key}&q={GetLocation(city)[0]},{GetLocation(city)[1]}"
        response = requests.get(url)

        return response.json()
   
    except Exception as e:
        print(f"Error Fetching Weather {e}")
        return None


def getTemp(api_key, city):
    try:
        data = fetchData(api_key, city)
        if data:
            raw_ctemp = data["current"]["feelslike_c"]

            ctemp = str(int(raw_ctemp))

            return ctemp
        return None
        
    except Exception as e:
        print(f"Error Fetching Temperature {e}")
        return None

def getCondition(api_key, city):
    try:
        data = fetchData(api_key, city)
        if data:
            current_condition = data["current"]["condition"]

            condition_icon_uri = current_condition["icon"]
            condition_text = current_condition["text"]

            return condition_text, condition_icon_uri
        return None, None
    except Exception as e:
        print(f"Error Fetching Condition {e}")
        return None, None
    
def checkDay(condition):
    if "day" in condition:
        return True
    elif "night" in condition:
        return False
    return False


def main():
    print("Starting weather monitor")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            api_key, city, update_interval = loadConfig()

            ctemp = getTemp(api_key, city)

            condition_text, condition_icon_uri = getCondition(api_key, city)

            print(checkDay(condition_icon_uri))
            
            if ctemp:
                ctemp += "ºC"
                print(f"Temperature: {ctemp}ºC | Condition: {condition_text}")
            else:
                print("Could not fetch weather")
            time.sleep(update_interval)

    except KeyboardInterrupt:
        print("\nMonitoring Stopped")

main()