from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request

from weather.models.account_model import User
from weather.models.favorites_manager import FavoritesManager

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

favorites_manager = FavoritesManager()

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


@app.route('/api/clear-favorites', methods=['DELETE'])
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
    