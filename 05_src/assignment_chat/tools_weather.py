from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os
from utils.logger import get_logger

_logs = get_logger(__name__)

load_dotenv('.secrets')

@tool
def get_weather(location: str='Toronto', units: str='m') -> str:
    """
    Returns weather information for a given location.
    Example:
    location: "New York", "London, UK", "51.5074,-0.1278", etc.
    units: "m" for Metric, "s" for Scientific, "f" for Fahrenheit.
    """
    url = "https://api.weatherstack.com/current"
    params = {
        "access_key": os.getenv('WEATHERSTACK_API_KEY'),
        "query": location,
        "units": units
    }

    try:
        response = requests.get(url, params=params)

        resp_dict = response.json()

        if "error" in resp_dict:
            error_info = resp_dict.get("error", {})
            error_message = error_info.get("info", "Unknown API error")
            _logs.error(f"Weather API error for {location}: {error_message}")
            return f"Could not retrieve weather information"
                
        current = resp_dict.get("current", {})

        if current:
            temperature = current.get("temperature")
            feelslike = current.get("feelslike")
            descriptions = ",".join(current.get("weather_descriptions", []))
            description = ", ".join(descriptions) if descriptions else "No description available"
            weather = (
                f"The weather in {location} is {description} "
                f"with a temperature of {temperature} degrees, "
                f"but it feels like {feelslike} degrees."
            )            
        else:
            weather = "Could not retrieve weather information."
            _logs.error(f"Could not retrieve weather information for {location}.")
    except Exception as e:
        _logs.error(f"Error occurred while fetching weather information: {e}")
        weather = "Could not retrieve weather information."
    return weather

