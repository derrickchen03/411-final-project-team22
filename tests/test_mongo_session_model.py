import pytest

from weather.models.mongo_session_model import MongoSessionModel


@pytest.fixture
def sample_user_id():
    return 1  # Primary key for user


@pytest.fixture
def sample_favorites():
    return {"favorite_id": 1, "weather": {"temp": 80, "wind": 12}, "favorite_id": 2, "weather": {"temp": 45, "wind": 9}}  # Sample weather data


def test_login_user_creates_session_if_not_exists(mocker, sample_user_id):
    """Test login_user creates a session with no combatants if it does not exist."""
    mock_find = mocker.patch("clients.mongo_client.sessions_collection.find_one", return_value=None)
    mock_insert = mocker.patch("clients.mongo_client.sessions_collection.insert_one")
    mock_favorites = mocker.Mock()

    MongoSessionModel.login_user(sample_user_id, mock_favorites)

    mock_find.assert_called_once_with({"user_id": sample_user_id})
    mock_insert.assert_called_once_with({"user_id": sample_user_id, "favorites": {}})
    mock_favorites.clear.assert_not_called()

def test_login_user_loads_favorites_if_session_exists(mocker, sample_user_id, sample_favorites):
    """Test login_user loads favorites if session exists."""
    mock_find = mocker.patch(
        "clients.mongo_client.sessions_collection.find_one",
        return_value={"user_id": sample_user_id, "favorites": sample_favorites}
    )
    mock_favorites = mocker.Mock()

    MongoSessionModel.login_user(sample_user_id, mock_favorites)

    mock_find.assert_called_once_with({"user_id": sample_user_id})
    mock_favorites.clear_combatants.assert_called_once()
    mock_favorites.prep_combatant.assert_has_calls([mocker.call(favorite) for favorite in sample_favorites])

def test_logout_user_updates_combatants(mocker, sample_user_id, sample_favorites):
    """Test logout_user updates the combatants list in the session."""
    mock_update = mocker.patch("clients.mongo_client.sessions_collection.update_one", return_value=mocker.Mock(matched_count=1))
    mock_favorites_manager = mocker.Mock()
    mock_favorites_manager.get_all_favorites_current_weather.return_value = sample_favorites

    MongoSessionModel.logout_user(sample_user_id, mock_favorites_manager)

    mock_update.assert_called_once_with(
        {"user_id": sample_user_id},
        {"$set": {"favorites": sample_favorites}},
        upsert=False
    )
    mock_favorites_manager.clear_favorites.assert_called_once()

def test_logout_user_raises_value_error_if_no_user(mocker, sample_user_id, sample_favorites):
    """Test logout_user raises ValueError if no session document exists."""
    mock_update = mocker.patch("clients.mongo_client.sessions_collection.update_one", return_value=mocker.Mock(matched_count=0))
    mock_favorites_manager = mocker.Mock()
    mock_favorites_manager.get_all_favorites_current_weather.return_value = sample_favorites

    with pytest.raises(ValueError, match=f"User with ID {sample_user_id} not found for logout."):
        MongoSessionModel.logout_user(sample_user_id, mock_battle_model)

    mock_update.assert_called_once_with(
        {"user_id": sample_user_id},
        {"$set": {"combatants": sample_combatants}},
        upsert=False
    )