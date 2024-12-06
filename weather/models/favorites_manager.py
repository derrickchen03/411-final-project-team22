from dataclasses import dataclass
import logging
import sqlite3
from typing import Any
#import requests
#from dotenv import load_dotenv
#import os

from account_model import User

from utils.logger import configure_logger

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
        self.favorites: dict[str, Any] = {}  # dictionary of favorite locations

    def add_favorite(self, location: str, temp: float, wind: float, precipitation: float, humidity: int) -> None:
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
            return self.favorites[favorite_loc]
        else:
            raise ValueError(f"{favorite_loc} not found in Favorites.")

    def get_all_favorites_current_weather(self) -> list[dict]:
        """
        Get the temperature for all of the user's favorite locations.

        Returns:
            list[dict]: a list of dictionaries containing the location and the temperature for that location.
        """
        temps = {}
        for location in self.favorites:
            temps[location] = self.favorites[location]["temp"]
        
        return temps

    def get_all_favorites(user_id: int) -> list[str]:
        """
        Get a list of all the favorite locations the user has saved.

        Args:
            user_id (int): the ID of the user currently logged in.

        Returns:
            list[str]: a list of the favorite locations saved by the user.
        """
        pass

    def get_favorite_historical(user_id: int, favorite: str) -> dict: 
        """
        Get the historical temperature, wind, precipitation, and humidity for a favorite location.

        Args:
            user_id (int): the ID of the user currently logged in.
            favorite (str): the location of the historical weather to be retrieved.

        Returns:
            dict: a dictionary containing the historical weather for the favorite location.
        """
        pass
    
    def get_favorites_forecast_5_days(self, location: str) -> 