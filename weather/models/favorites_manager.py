from dataclasses import dataclass
import logging
import sqlite3
from typing import Any
import requests

from account_model import User

from utils.logger import configure_logger

logger = logging.getLogger(__name__)
configure_logger(logger)

def add_favorite(user_id: int, location: str) -> None:
    """
    Add a new favorite by the location to the user's favorites.

    Args:
        user_id (int): the id for the user currently logged in.
        location (str): the location to be added to the favorites.
    """
    


    pass

def get_favorite_weather(user_id: int, favorite: str) -> dict:
    """
    Get the realtime temperature, wind, precipitation, and humidity for a favorite location. 

    Args:
        user_id (int): the id of the user currently logged in.
        favorite (str): the location of the weather to be retrieved.

    Returns: 
        dict: a dictionary containing the realtime weather for the favorite location.
    """
    url = f'http://api.weatherapi.com/v1/current.json?key={KEY_VALUE}&q={favorite}'
    response = requests.get(url)
    
    pass

def get_all_favorites_current_weather(user_id: int) -> list[dict]:
    """
    Get the temperature for all of the user's favorite locations.

    Args:
        user_id (int): the ID of the user that's logged in

    Returns:
        list[dict]: a list of dictionaries containing the location and the temperature for that location.
    """
    pass

def get_all_favorites(user_id: int) -> list[str]:
    """
    Get a list of all the favorite locations the user has saved.

    Args:
        user_id (int): the ID of the user currently logged in.

    Returns:
        list[str]: a list of the favorite locations saved by the user.
    """
    pass

def get_favorite_historical(user_id: int, favorite: str) -> dict: #History Object returned by the api
    """
    Get the historical temperature, wind, precipitation, and humidity for a favorite location.

    Args:
        user_id (int): the ID of the user currently logged in.
        favorite (str): the location of the historical weather to be retrieved.

    Returns:
        dict: a dictionary containing the historical weather for the favorite location.
    """
    pass