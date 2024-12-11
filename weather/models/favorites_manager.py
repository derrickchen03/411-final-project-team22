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

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = "http://api.weatherapi.com/v1"

logger = logging.getLogger(__name__)
configure_logger(logger)

class FavoritesModel:
    """
    A class to manage the user's favorites.

    Attributes:
        favorites (dict[str, Any]): The dictionary containing the weather for each of the user's favorite locations.
    """

    def __init__(self):
        """Initializes the FavoritesManager with an empty list of favorites."""
        self.favorites: dict[str, dict[str, Any]] = {}  # dictionary of favorite locations


    def get_weather_api(self, location):
        """
        Get the current weather for a location.

        Args:
            location (str): the location to retrieve the weather for.
        
        Return:
            temp (float): the location's temperature in Farenheit.
            wind (float): the location's wind in mph.
            precipitation (float): the location's preciptation in inches.
            humidity (int): the location's humidity.
        """
        # call the current weather api
        url = f'{weather_api}/current.json?key={api_key}&q={location}'
        response = requests.get(url)

        # parse through the response to get the values we will save.
        weather = response.json()['current']
        temp = weather['temp_f']
        wind = weather['wind_mph']
        precipitation = weather['precip_in']
        humidity = weather['humidity']
        return temp, wind, precipitation, humidity       

    def add_favorite(self, location: str, temp: float, wind: float = None, precipitation: float = None, humidity: int = None) -> None:

        """Initializes the FavoritesModel with an empty list of favorites."""
        self.favorites: dict[str, Any] = {}  # dictionary of favorite locations

        """
        Add a new favorite by the location to the user's favorites.

        Args:
            location (str): the location to be added to the favorites.
            temp (float): the location's temperature in Farenheit.
            wind (float): the location's wind speed in miles per hour.
            precipitation (float): the location's precipitation in inches.
            humidity (int): the location's humidity.

        Raises:
            ValueError: if the temp, wind, precipitation, humidity are not floats or None.
        """
        
        

        if not isinstance(temp, float) or temp == None:
            raise ValueError(f"Invalid temperature: {temp}, should be a float.")
        if not isinstance(wind, float) or wind == None:
            raise ValueError(f"Invalid wind: {wind}, should be a float.")
        if not isinstance(precipitation, float) or precipitation == None:
            raise ValueError(f"Invalid precipitation: {precipitation}, should be a float.")
        if not isinstance(humidity, int) or humidity == None:
            raise ValueError(f"Invalid humidity: {humidity}, should be an int.")
        

        logger.info("Adding weather for %s to favorites.", location)
        self.favorites[location] = {'temp': temp, 'wind': wind, 'precipitation': precipitation, 'humidity': humidity}
        return

    def clear_favorites(self) -> None:
        """
        Clear the dictionary of the user's favorited weather locations.
        """
        logger.info("Clearing the favorites dictionary.")
        self.favorites.clear()


    def get_favorite_weather(self, location: str) -> dict:
        """
        Get the realtime temperature, wind, precipitation, and humidity for a favorite location. 

        Args:
            location (str): the location of the weather to be retrieved.

        Returns: 
            dict: a dictionary containing the realtime weather for the favorite location.
        
        Raises:
            ValueError: if the location has not been saved in the Favorites dictionary.
        """
        
        logger.info("retrieving weather from %s.", location)

        if location in self.favorites:
            try:
                query = {"key": api_key, "q": f"{location}"}
                response = requests.get(weather_api + "/current.json", params = query)
                if response.status_code != 200:
                    return {'status': 'failed', 'error': '1006', 'message': 'location not found'}
                else:
                    parsed = response.json()
                    self.favorites[location]['temp'] = parsed['current']['temp_f']
                    self.favorites[location]['wind'] = parsed['current']['wind_mph']
                    self.favorites[location]['precipitation'] = parsed['current']['precip_in']
                    self.favorites[location]['humidity'] = parsed['current']['humidity']
                return self.favorites[location]
            except:
                return {'status': 'failed', 'error': f'{response.status_code}', 'message': 'error occurred when retrieving location'}
        else:
            raise ValueError(f"{location} not found in Favorites.")

    def get_all_favorites_current_weather(self) -> list[dict]:
        """
        Get the temperature data for all of the user's favorite locations.

        Returns:
        list[dict]: a list of dictionaries containing the locations and the temperature for that location.

        Raises:
            ValueError: If the favorites dictionary is empty.

        """
        logger.info("Retrieving current temperature for all favorites")
        if len(self.favorites) == 0:
            raise ValueError("No locations saved in favorites.")
        
        temps = {}
        for location in self.favorites:
            logger.info(f"Retrieving current temperature for {location}")
            try:
                query = {"key": api_key, "q": f"{location}"}
                response = requests.get(weather_api + "/current.json", params = query)
                if response.status_code != 200:
                    return {'status': 'failed', 'error': f'{response.status_code}'}
                else:
                    parsed = response.json()
                    temps[location] = parsed['current']['temp_f']
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving location'}
        return temps

    def get_all_favorites(self) -> list[str]:
        """
        Get a list of all the favorite locations the user has saved.

        Returns:
            list[str]: a list of the favorite locations saved by the user.

        Raises:
            ValueError: if the favorites dictionary is empty.
        """
        logger.info("Fetching the list of all favorites")
        if len(self.favorites) == 0:
            raise ValueError("Favorites dictionary is empty.")
        
        return self.favorites.keys()

    def get_favorite_historical(self, location: str) -> dict: 
        """
        Get the historical temperature, wind, precipitation, and humidity for a favorite location, for up to 5 days in the past, not including current.

        Args:
            location (str): the location of the historical weather to be retrieved.
            temp (float): the location's temperature in Farenheit.
            wind (float): the location's wind speed in miles per hour.
            precipitation (float): the location's precipitation in inches.
            humidity (int): the location's humidity.

        Returns:
            dict: a dictionary containing the historical weather for the favorite location.

        Raises:
            ValueError: if the location has not be saved in favorites.
        """
        logger.info("Fetching the historical data for a favorite location")
        historical_data = {}
        if location in self.favorites:
            try:
                for i in range(1,5):
                    datex = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                    query = {"key": api_key, "q": f"{location}", 'dt': datex}
                    response = requests.get(weather_api + "/history.json", params = query)
                    if response.status_code != 200:
                        return {'status': 'failed', 'error': f'{response.status_code}'}
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
    
    def get_all_favorite_historical(self) -> dict:
        """
        Get all historical weather for all favorite locations.

        Returns:
            dict: a dictionary containing all historical weather for all locations
        """
        logger.info("Fetching the historical data for the list of favorite locations")
        historical_data_all = {}
        
        if len(self.favorites) < 1:
            return {'error': 'no favorites found'}
        else:
            for location in self.favorites:
                logger.info(f"Fetching the historical data for {location}")
                historical_data_all[location] = self.get_favorite_historical(location)
        return historical_data_all

    def get_favorite_next_day_forecast(self, location: str) -> dict:
        """
        Get the next day forecast for a favorite location.

        Args:
            location (str): the location of the forecast to be retrieved.

        Returns:
            dict: a dictionary of the average temperature for each day.
        """
        logger.info(f"Retrieving next day forecast for {location}.")
        if location in self.favorites:
            try:
                query = {"key": api_key, "q": f"{location}", 'days': 2}
                response = requests.get(weather_api + "/forecast.json", params = query)
                
                if response.status_code != 200:
                            return {'status': 'failed', 'error': f'{response.status_code}'}
                else:
                    parsed = response.json()
                    next_day_forecast = parsed['forecast']['forecastday'][1]
                    date = next_day_forecast['date']
                    maxtemp = next_day_forecast['day']['maxtemp_f']
                    mintemp = next_day_forecast['day']['mintemp_f']
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving location'}
        else:
            raise ValueError(f"{location} not found in Favorites.")
        return {"date": date, "max_temp": maxtemp, "min_temp": mintemp}

        
    def get_all_favorites_next_day_forecast(self) -> dict:
        """
        Get all next day forecasts for all favorite locations.

        Returns:
            dict: a dictionary with all next day forecasts for all locations.
        """
        
        logger.info("Retrieving next day forecast for all favorites")
        forecast_data_all = {}
        
        if len(self.favorites) < 1:
            raise ValueError("No locations saved in favorites.")
        else:
            try:
                for location in self.favorites:
                    logger.info(f"Fetching the forecast data for {location}")
                    forecast_data_all[location] = self.get_favorite_next_day_forecast(location)
            except Exception as e:
                logger.error(f"Error fetching forecast data for {location}: {e}")
                forecast_data_all[location] = {'status': 'failed', 'error': 'UnhandledException', 'message': str(e)}
                
        return forecast_data_all
    
    def get_favorite_alerts(self, location: str) -> dict:
        """
        Gets alert data for a favorite location.

        Args:
            location (str): the location of alert data to be retrieved.

        Returns:
            dict: a dictionary with alert data for the weather location
        """
        logger.info(f"Fetching the alert data for a favorite location, {location}")
        if location in self.favorites:
            try:
                query = {"key": api_key, "q": f"{location}"}
                response = requests.get(weather_api + "/alerts.json", params = query)
                if response.status_code != 200:
                            return {'status': 'failed', 'error': f'{response.status_code}'}
                parsed = response.json()
                if 'alerts' not in parsed or 'alert' not in parsed['alerts']:
                    return {'alert': 'none'}
                alerts = parsed['alerts']['alert']
                return {'alert': alerts}
            except:
                return {'status': 'failed', 'error': 400, 'message': 'error occurred when retrieving location'}
        else:
            raise ValueError(f"{location} not found in Favorites.")
    
    def get_all_favorite_alerts(self) -> dict:
        """
        Gets alert data for all favorite locations.

        Returns:
            dict: dictionary containing all alerts for favorite locations.
        """
        logger.info("Fetching the alert data for all favorites")
        alert_data_all = {}
        if len(self.favorites) < 1:
            raise ValueError("No locations saved in favorites.")
        else:
            try:
                for location in self.favorites:
                    logger.info(f"Fetching the alert data for {location}")
                    alert_data_all[location] = self.get_favorite_alerts(location)
            except Exception as e:
                logger.error(f"Error fetching alert data for {location}: {e}")
                alert_data_all[location] = {'status': 'failed', 'error': 'UnhandledException', 'message': str(e)}
        return alert_data_all
    
    def get_favorite_coordinates(self, location: str) -> dict:
        """
        Gets coordinates for a favorite location.

        Args:
            location (str): the location of whose coordinates will be retrived. 

        Returns:
            dict: a dictionary with coordinates of the favorite location
        """
        
        logger.info(f"Retrieving coordinate data for {location} in favorites")
        if location in self.favorites:
            try:
                query = {"key": api_key, "q": f"{location}"}
                response = requests.get(weather_api + "/timezone.json", params = query)
                
                if response.status_code != 200:
                            return {'status': 'failed', 'error': f'{response.status_code}'}
                else:
                    parsed = response.json()
                    lat = parsed['location']['lat']
                    lon = parsed['location']['lon']

            except Exception as e:
                logger.error(f"Error occurred when retrieving coordinates for {location}: {e}")
                return {'status': 'failed', 'error': 400, 'message': 'Error occurred when retrieving location'}
        else:
            raise ValueError(f"{location} not found in Favorites.")
        return {"lattitude": lat, "longitude": lon}
    
    def get_all_favorite_coordinates(self) -> dict:
        """
        Gets coordinates for all favorite locations.

        Returns:
            dict: a dictionary with all coordinates of favorite locations.
        """
        logger.info("Fetching the alert data for all favorites")
        coordinate_data_all = {}
        if len(self.favorites) < 1:
            raise ValueError("No locations saved in favorites.")
        else:
            try:
                for location in self.favorites:
                    logger.info(f"Fetching the coordinate data for {location}")
                    coordinate_data_all[location] = self.get_favorite_coordinates(location)
            except Exception as e:
                logger.error(f"Error fetching alert data for {location}: {e}")
                coordinate_data_all[location] = {'status': 'failed', 'error': 'UnhandledException', 'message': str(e)}
        return coordinate_data_all