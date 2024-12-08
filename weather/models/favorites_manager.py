from dataclasses import dataclass
from dotenv import load_dotenv
import json
import logging
import sqlite3
from typing import Any
import requests
import os
from datetime import datetime, timedelta
from utils.logger import configure_logger

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = "http://api.weatherapi.com/v1"

logger = logging.getLogger(__name__)
configure_logger(logger)

class FavoritesManager:
    """
    A class to manage the user's favorites.

    Attributes:
        favorites (dict[str, Any]): The dictionary containing the weather for each of the user's favorite locations.
    """

    def __init__(self):
        """Initializes the FavoritesManager with an empty list of favorites."""
        self.favorites: dict[str, dict[str, Any]] = {}  # dictionary of favorite locations

    def add_favorite(self, location: str, temp: float = None, wind: float = None, precipitation: float = None, humidity: int = None) -> None:
        """
        Add a new favorite by the location to the user's favorites.

        Args:
            location (str): the location to be added to the favorites.
            temp (float): the location's temperature in Farenheit.
            wind (float): the location's wind speed in miles per hour.
            precipitation (float): the location's precipitation in inches.
            humidity (int): the location's humidity.
        """
        
        logger.info("Adding weather for %s to favorites.", location)
        self.favorites[location] = {'temp': temp, 'wind': wind, 'precipitation': precipitation, 'humidity': humidity}
        return

    def clear_favorites(user_id: int, favorites: dict) -> None:
        """
        Clear the dictionary of the user's favorited weather locations.

        Args:
            user_id (int): the id for the user currently logged in.
            favorites (dict): the dictionary of the user's saved locations.
        """
        
        favorites.clear()


    def get_favorite_weather(self, favorite_loc: str) -> dict:
        """
        Get the realtime temperature, wind, precipitation, and humidity for a favorite location. 

        Args:
            user_id (int): the id of the user currently logged in.
            favorite (str): the location of the weather to be retrieved.

        Returns: 
            dict: a dictionary containing the realtime weather for the favorite location.
        
        Raises:
            ValueError: if the location has not been saved in the Favorites dictionary.
        """
        
        logger.info("retrieving weather from %s.", favorite_loc)

        if favorite_loc in self.favorites:
            try:
                query = {"key": api_key, "q": f"{favorite_loc}"}
                response = requests.get(weather_api + "/current.json", params = query)
                if response.get_status != 200:
                    return {'status': 'failed', 'error': '1006', 'message': 'location not found'}
                else:
                    parsed = json.loads(response)
                    self.favorites[favorite_loc]['temp'] = parsed['current']['temp_f']
                    self.favorites[favorite_loc]['wind'] = parsed['current']['wind_mph']
                    self.favorites[favorite_loc]['precipitation'] = parsed['current']['precip_in']
                    self.favorites[favorite_loc]['humidity'] = parsed['current']['humidity']
                return self.favorites[favorite_loc]
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving loc'}
        else:
            raise ValueError(f"{favorite_loc} not found in Favorites.")

    def get_all_favorites_current_weather(self) -> list[dict]:
        """
        Get the temperature data for all of the user's favorite locations.

        Returns:
            list[dict]: a list of dictionaries containing the locations and the temperature for that location.
        """
        temps = {}
        for location in self.favorites:
            try:
                query = {"key": api_key, "q": f"{location}"}
                response = requests.get(weather_api + "/current.json", params = query)
                if response.get_status != 200:
                    return {'status': 'failed', 'error': '1006', 'message': 'location not found'}
                else:
                    parsed = json.loads(response)
                    temps[location] = parsed['current']['temp_f']
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving location'}
        return temps

    def get_all_favorites(self) -> list[str]:
        """
        Get a list of all the favorite locations the user has saved.

        Returns:
            list[str]: a list of the favorite locations saved by the user.
        """
        fav_locations = []

        for location in self.favorites:
            fav_locations.append(location)
        
        return fav_locations

    def get_favorite_historical(self, location: str) -> dict: 
        """
        Get the historical temperature, wind, precipitation, and humidity for a favorite location, for up to 5 days in the past, not including current.

        Args:
            location (str): the location to be added to the favorites.
            temp (float): the location's temperature in Farenheit.
            wind (float): the location's wind speed in miles per hour.
            precipitation (float): the location's precipitation in inches.
            humidity (int): the location's humidity.

        Returns:
            dict: a dictionary containing the historical weather for the favorite location.

        Raises:
            ValueError: if the location has not be saved in favorites.
        """
        historical_data = {}
        if location in self.favorites:
            try:
                for i in range(1,5):
                    datex = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                    query = {"key": api_key, "q": f"{location}", 'dt': datex}
                    response = requests.get(weather_api + "/history.json", params = query)
                    if response.get_status != 200:
                        return {'status': 'failed', 'error': '1006', 'message': 'location not found'}
                    else:
                        parsed = response.json()
                        forecast = parsed['forecast']['forecastday'][0]['day']
                        historical_data[datex] = {
                            'temp': forecast['avgtemp_f'],
                            'wind': forecast['maxwind_mph'],
                            'precipitation': forecast['totalprecip_in'],
                            'humidity': forecast['avghumidity']
                        }
                return {f'{location}':historical_data}
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving location'}
        else:
            raise ValueError(f"{location} not found in Favorites.")
    

    def get_favorites_forecast_5_days(self, location: str) -> dict:
        pass