import requests
import os

from dotenv import load_dotenv, dotenv_values

load_dotenv()

api_key = os.getenv("WEATHER_API")

print(f"{api_key}")