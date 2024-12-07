import pytest

from weather.models.favorites_manager import FavoritesModel

@pytest.fixture
def favorites_model():
    """Fixture to provide a new instance of FavoritesModel for each test."""
    return FavoritesModel()

# Fixture providing a sample favorites dictionary
@pytest.fixture
def sample_favorites():
    return {
        "Boston": 
        {
            "temp": 32.0,
            "wind": 12.0,
            "precipitation": 3.5,
            "humidity": 20
        },
        "New York": {
            "temp": 45.0,
            "wind": 5.3,
            "precipitation": 10.0,
            "humidity": 27
        }
    }

def test_add_favorite():
    """testing adding a location to the favorites dictionary."""
    favorites_model.add_favorite("Boston", 32.0, 12.0, 3.5, 20)
    assert len(favorites_model.favorites) == 1
    assert favorites_model.favorites[0] == 'Boston'
    pass

def test_add_favorite_invalid_temp():
    """Test error when adding a location with an invalid temperature """
    pass

def test_add_favorite_invalid_wind():
    """Test error when adding a location with an invalid wind value."""
    pass

def test_add_favorite_invalid_precipitation():
    """Test error when adding a location with an invalid precipitation value."""
    pass

def test_clear_favorites(favorites_manager, sample_favorites):
    """Test that clear_favorites empties the dictionary."""
    favorites_manager.favorites.extend(sample_favorites)

    # Call the clear_favorites method
    favorites_manager.clear_favorites()

    # Assert that the favorites dictionary is now empty
    assert len(favorites_manager.favorites) == 0, "Favorties dictionary should be empty after calling clear_favorites."

def test_clear_favorites_empty(favorites_manager):
    """Test that calling clear_favorites on an empty dictionary works."""

    # Call the clear_favorites method with an empty dictionary
    favorites_manager.clear_favorites()

    # Assert that the favorites dictionary is still empty
    assert len(favorites_manager.favorites) == 0, "Favorites dictionary should remain empty if it was already empty."


