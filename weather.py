import requests
import os
import time
from geopy.geocoders import Nominatim
from dotenv import load_dotenv


class WeatherMonitor:
    def __init__(self):
        self.api_key, self.city, self.update_interval = self.load_config()
        self.ctemp = None
        self.condition_text = None
        self.condition_icon_uri = None
        self.is_daytime = None

    def load_config(self):
        env_vars = ["WEATHER_API", "CITY", "UPDATE_INTERVAL"]

        for var in env_vars:
            if var in os.environ:
                del os.environ[var]

        load_dotenv(override=True)
        api_key = os.getenv("WEATHER_API")
        city = os.getenv("CITY")
        update_interval = float(os.getenv("UPDATE_INTERVAL"))

        return api_key, city, update_interval

    def get_location(self):
        geolocator = Nominatim(user_agent="smart-clock")
        location = geolocator.geocode(self.city)
        lat = f"{location.latitude:.3f}"
        lon = f"{location.longitude:.3f}"
        return lat, lon

    def fetch_data(self):
        """Fetch current weather for the city"""
        try:
            method = "current"
            base_uri = "https://api.weatherapi.com/v1"
            lat, lon = self.get_location()
            url = f"{base_uri}/{method}.json?key={self.api_key}&q={lat},{lon}"
            response = requests.get(url)
            return response.json()
        except Exception as e:
            print(f"Error Fetching Weather {e}")
            return None

    def update_weather(self):
        """Update temperature, condition, and daytime info"""
        try:
            data = self.fetch_data()
            if not data:
                return False

            raw_ctemp = data["current"]["feelslike_c"]
            self.ctemp = f"{int(raw_ctemp)}ºC"

            condition = data["current"]["condition"]
            self.condition_text = condition["text"]
            self.condition_icon_uri = condition["icon"]

            self.is_daytime = "day" in self.condition_icon_uri

            return True
        except Exception as e:
            print(f"Error Updating Weather {e}")
            return False

    def run(self):
        """Run continuous weather monitoring"""
        print("Starting weather monitor")
        print("Press Ctrl+C to stop\n")

        try:
            while True:
                if self.update_weather():
                    print(
                        f"Temperature: {self.ctemp} | "
                        f"Condition: {self.condition_text} | "
                        f"Daytime: {self.is_daytime}"
                    )
                else:
                    print("Could not fetch weather")
                time.sleep(self.update_interval)

        except KeyboardInterrupt:
            print("\nMonitoring Stopped")


if __name__ == "__main__":
    monitor = WeatherMonitor()
    monitor.run()