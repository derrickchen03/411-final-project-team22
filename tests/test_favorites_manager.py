import pytest
import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime, timedelta

from weather.models.favorites_manager import FavoritesModel

load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = "http://api.weatherapi.com/v1"

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of FavoritesModel for each test."""
    return FavoritesModel()

# Fixture providing a sample favorites dictionary
@pytest.fixture
def sample_favorites():
    sample_favs = {'Boston': {}, 'New York': {}}

    query = {"key": api_key, "q": "Boston"}
    response = requests.get(weather_api + "/current.json", params = query)
    
    parsed = response.json()
    sample_favs['Boston']['temp'] = parsed['current']['temp_f']
    sample_favs['Boston']['wind'] = parsed['current']['wind_mph']
    sample_favs['Boston']['precipitation'] = parsed['current']['precip_in']
    sample_favs['Boston']['humidity'] = parsed['current']['humidity']

    query = {"key": api_key, "q": "New York"}
    response = requests.get(weather_api + "/current.json", params = query)

    sample_favs['New York']['temp'] = parsed['current']['temp_f']
    sample_favs['New York']['wind'] = parsed['current']['wind_mph']
    sample_favs['New York']['precipitation'] = parsed['current']['precip_in']
    sample_favs['New York']['humidity'] = parsed['current']['humidity']
    return sample_favs
# Fixture providing historical weather
@pytest.fixture
def historical_favorites():
    historical_favs = {}

    for i in range(1,5):
        datex = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        query = {"key": api_key, "q": "Boston", 'dt': datex}
        response = requests.get(weather_api + "/history.json", params = query) 

        parsed = response.json()
        forecast = parsed['forecast']['forecastday'][0]['day']
        historical_favs[datex] = {
            'temp': forecast['avgtemp_f'],
            'wind': forecast['maxwind_mph'],
            'precipitation': forecast['totalprecip_in'],
            'humidity': forecast['avghumidity']
        }
    return {"Boston":historical_favs}

# Fixture providing next day forecast
@pytest.fixture
def next_day_forecast():
    query = {"key": api_key, "q": "Boston", 'days': 2}
    response = requests.get(weather_api + "/forecast.json", params = query)

    parsed = response.json()
    next_day_forecast = parsed['forecast']['forecastday'][1]
    date = next_day_forecast['date']
    maxtemp = next_day_forecast['day']['maxtemp_f']
    mintemp = next_day_forecast['day']['mintemp_f']

    return {"date": date, "max_temp": maxtemp, "min_temp": mintemp}

#Fixture providing alerts
@pytest.fixture
def favorite_alerts():
    query = {"key": api_key, "q": f"Boston"}
    response = requests.get(weather_api + "/alerts.json", params = query)

    parsed = response.json()
    alerts = parsed['alerts']['alert']
    return {'alert': alerts}

#Fixture providing coordinates
@pytest.fixture
def favorite_coordinates():
    query = {"key": api_key, "q": f"Boston"}
    response = requests.get(weather_api + "/timezone.json", params = query)
    
    parsed = response.json()
    lat = parsed['location']['lat']
    lon = parsed['location']['lon']
    return {"lattitude": lat, "longitude": lon}

####################################################################
#############        UNIT TESTS       ##############################
####################################################################

def test_add_favorite(favorites_model):
    """testing adding a location to the favorites dictionary."""
    favorites_model.add_favorite("Boston", 32.4, 12.3, 3.5, 20)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites['Boston'] == {'temp': 32.4, 'wind': 12.3, 'precipitation': 3.5, 'humidity': 20}
    

def test_add_favorite_invalid_temp(favorites_model):
    """Test error when adding a location with an invalid temperature """
    with pytest.raises(ValueError, match="Invalid temperature: 32, should be a float."):
        favorites_model.add_favorite("Boston", 32, 12.0, 3.5, 20)

def test_add_favorite_invalid_wind(favorites_model):
    """Test error when adding a location with an invalid wind value."""
    with pytest.raises(ValueError, match="Invalid wind: 12, should be a float."):
        favorites_model.add_favorite("Boston", 32.0, 12, 3.5, 20)

def test_add_favorite_invalid_precipitation(favorites_model):
    """Test error when adding a location with an invalid precipitation value."""
    with pytest.raises(ValueError, match="Invalid precipitation: 3, should be a float."):
        favorites_model.add_favorite("Boston", 32.0, 12.0, 3, 20)

def test_add_favorite_invalid_humidity(favorites_model):
    """Test error when adding a location with an invalid humidity value."""
    with pytest.raises(ValueError, match="Invalid humidity: 20.4, should be an int."):
        favorites_model.add_favorite("Boston", 32.0, 12.0, 3.5, 20.4)

def test_clear_favorites(favorites_model, sample_favorites):
    """Test that clear_favorites empties the dictionary."""
    favorites_model.favorites.update(sample_favorites)

    # Call the clear_favorites method
    favorites_model.clear_favorites()

    # Assert that the favorites dictionary is now empty
    assert len(favorites_model.favorites) == 0, "Favorties dictionary should be empty after calling clear_favorites."

def test_clear_favorites_empty(favorites_model):
    """Test that calling clear_favorites on an empty dictionary works."""

    # Call the clear_favorites method with an empty dictionary
    favorites_model.clear_favorites()

    # Assert that the favorites dictionary is still empty
    assert len(favorites_model.favorites) == 0, "Favorites dictionary should remain empty if it was already empty."

def test_get_favorite_weather(favorites_model, sample_favorites):
    """Test that get_favorite_weather retrieves the weather."""
    favorites_model.favorites.update(sample_favorites)

    # Call the function and verify the result
    favorites = favorites_model.get_favorite_weather('Boston')
    assert favorites == favorites_model.favorites['Boston'], "Expected get_favorites_weather to return the correct weather dictionary."

def test_get_favorite_weather_bad_location(favorites_model, sample_favorites):
    """Test retrieving the weather for a location that doesn't exist in the favorites dictionary"""
    favorites_model.favorites.update(sample_favorites)
    with pytest.raises(ValueError, match="Denver not found in Favorites."):
        favorites_model.get_favorite_weather("Denver")

def test_get_all_favorites_current_weather(favorites_model, sample_favorites):
    """Test successfullly retrieving the temperature data for each location in favorites."""
    favorites_model.favorites.update(sample_favorites)

    all_favorites = favorites_model.get_all_favorites_current_weather()
    assert len(all_favorites) == 2
    assert "Boston" in all_favorites.keys()
    assert "New York" in all_favorites.keys()

def test_get_all_favorites_current_weather_empty(favorites_model):
    """Test error is raised when favorites is empty."""
    favorites_model.clear_favorites()

    with pytest.raises(ValueError, match="No locations saved in favorites."):
        favorites_model.get_all_favorites_current_weather()

def test_get_all_favorites(favorites_model, sample_favorites):
    """Test successfully retrieving all locations from favorites."""
    favorites_model.favorites.update(sample_favorites)

    all_locations = favorites_model.get_all_favorites()
    assert len(all_locations) == 2
    assert "Boston" in all_locations
    assert "New York" in all_locations

def test_get_all_favorites_empty(favorites_model):
    """Test error is raised when favorites is empty."""
    favorites_model.clear_favorites()

    with pytest.raises(ValueError, match="Favorites dictionary is empty."):
        favorites_model.get_all_favorites()

def test_get_favorite_historical(favorites_model, historical_favorites, sample_favorites):
    """Test that get_favorite_historical gets the historical weather for the location."""
    favorites_model.favorites.update(sample_favorites)
    # Call the function and verify the result
    historical = favorites_model.get_favorite_historical('Boston')
    assert historical == historical_favorites, "Expected get_favorites_historical to return the correct weather dictionary."

def test_get_favorite_historical_bad_location(favorites_model):
    """Test error is rased when the location is not in favorites."""

    with pytest.raises(ValueError, match="Denver not found in Favorites."):
        favorites_model.get_favorite_historical("Denver")

def test_get_favorite_next_day_forecast(favorites_model, next_day_forecast, sample_favorites):
    """Test that get_favorite_next_day_forecast gets the weather for the following day."""
    favorites_model.favorites.update(sample_favorites)
    # Call the function and verify the result
    forecast = favorites_model.get_favorite_next_day_forecast("Boston")
    assert forecast == next_day_forecast, "Expected get_favorite_next_day_forecast to return the correct weather dictionary."

def test_get_favorite_alerts(favorites_model, favorite_alerts, sample_favorites):
    """Test that get_favorite_alerts gets the alerts for the location."""
    favorites_model.favorites.update(sample_favorites)
    # Call the function and verify the result
    alerts = favorites_model.get_favorite_alerts("Boston")
    assert alerts == favorite_alerts, "Expected get_favorites_alerts to return the correct alert dictionary."

def test_get_favorite_coordinates(favorites_model, favorite_coordinates, sample_favorites):
    """Test that get_favorite_coordinates gets the correct coordinates for a location."""
    favorites_model.favorites.update(sample_favorites)
    #Call the function and verify result
    coordinates = favorites_model.get_favorite_coordinates("Boston")
    assert coordinates == favorite_coordinates, "Expected get_favorites_coordinates to return the correct coordinates dictionary."

