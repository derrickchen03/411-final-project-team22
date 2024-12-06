from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request

from weather.models.account_model import User
from weather.models.favorites_manager import FavoritesManager

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

favorites_manager = FavoritesManager()

####################################################
#
# Healthchecks
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.

    Returns:
        JSON response indicating the health status of the service.
    """
    app.logger.info('Health check')
    return make_response(jsonify({'status': 'healthy'}), 200)

##########################################################
#
# Favorites Management
#
##########################################################

@app.route('/api/add-favorite', methods=['POST'])
def add_favorite() -> Response:
    """
    Route to add a favorite to user's list of favorites.

    Expected JSON Input:
        - user_id (int): the id for the user currently logged in.
        - location (str): the location to be added to the favorites.

    Returns:
    JSON response indicating the success of the favorite addition.
    """
    app.logger.info("Adding a new favorite to list of user's favorites")


@app.route('/api/clear-favorites/<int:user_id>', methods=['DELETE'])
def clear_favorites(user_id: int) -> Response:
    """
    Route to clear the dictionary of the user's favorite weather locations.
    
    Path Parameter:
        - user_id (int): the id for the user currently logged in.
    Returns:
        JSON response indicuating success of the operation or error message.
    """
    try: 
        app.logger.info("Clearing weather favorites of user {user_id}" )
        favorites_manager.clear_favorites(user_id, favorites_manager.favorites)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        app.logger.error(f"Error clearing favorites: {e}")
        return make_response(jsonify({'error': str(e)}), 500)
    
@app.route('/api/get-favorite-weather/<int:user_id>', methods=['GET'])
def get_weather(user_id: int) -> Response:
    """
    Route to get the weather of a favorite location

    Path Parameter: 
        - user_id (int): the id for the user currently logged in.
    """

@app.route('/api/get-all-favorites-current-weather/<int:user_id>', methods=['GET'])
def get_all_favorites_weather(user_id: int) -> Response:
    """
    Route to get the temperature for all the user's favorite locations.
    """

@app.route('/api/get-all-favorites/<int:user_id>', method=['GET'])
def get_all_favorites(user_id: int) -> Response:
    """
    Route to get all the favorite locations of the user.
    """

@app.route('/api/get-favorite-historical/<int:user_id>',  method=['GET'])
def get_favorite_historical(user_id: int) -> Response:
    """"
    Route to get the historical temperature, wind, precipitation, and humidity for a favorite location.
    """