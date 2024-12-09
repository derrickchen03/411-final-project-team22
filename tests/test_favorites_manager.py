import pytest
import requests
import os
import json

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
    sample_favs = {}

    query = {"key": api_key, "q": "Boston"}
    response = requests.get(weather_api + "/current.json", params = query)
    
    parsed = json.loads(response)
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

def test_add_favorite():
    """testing adding a location to the favorites dictionary."""
    favorites_model.add_favorite("Boston", 32.0, 12.0, 3.5, 20)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0] == 'Boston'
    

def test_add_favorite_invalid_temp():
    """Test error when adding a location with an invalid temperature """
    pass

def test_add_favorite_invalid_wind():
    """Test error when adding a location with an invalid wind value."""
    pass

def test_add_favorite_invalid_precipitation():
    """Test error when adding a location with an invalid precipitation value."""
    pass

def test_clear_favorites(favorites_model, sample_favorites):
    """Test that clear_favorites empties the dictionary."""
    favorites_model.favorites.extend(sample_favorites)

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

def test_get_favorite_weather(favorites_model):
    """Test that get_favorite_weather retrieves the weather."""
    favorites_model.favorites.extend(sample_favorites)

    # Call the function and verify the result
    favorites = favorites_model.get_favorite_weather('Boston')
    assert favorites == favorites_model.favorites['Boston'], "Expected get_favorites_weather to return the correct weather dictionary."
