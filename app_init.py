from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
from sqlalchemy.sql import text
import sqlite3

from config import ProductionConfig
from db import db
from weather.models.account_model import User
from weather.models.favorites_manager import FavoritesModel
import requests
import os

# Load environment variables from .env file
load_dotenv()

# Don't think we need these here
#api_key = os.getenv("API_KEY")
#weather_api = "http://api.weatherapi.com/v1"

# Initialize SQLLite SQLAlchemy DB through Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)






with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e)
favorites_manager = FavoritesModel()
        
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
    app.logger.info('Initiating Health check')
    try:
        query = {"key": api_key, "q": "London"}
        response = requests.get(weather_api + "/current.json", params = query, timeout = 5)
        if response.status_code == 200:
            return make_response(jsonify({'status': 'healthy'}), 200)
        else:
            return make_response(jsonify({'status': 'failed'}), 503)
    except Exception as e:
        return make_response(jsonify({'status': 'failed'}), 503)
    
# Don't think we need this either, it's not in the project description
@app.route('/api/db-check', methods=['GET'])
def db_check() -> Response:
    """
    Route to check if the database connection and meals table are functional.

    Returns:
        JSON response indicating the database health status.
    Raises:
        404 error if there is an issue with the database.
    """
    app.logger.info("Checking database connection...")
    try:
        db.session.execute(text("SELECT 1"))
        app.logger.info("Database connection is OK.")
        return make_response(jsonify({'database_status': 'healthy'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 404)
    
if __name__ == '__main__':
    app.run(debug=True)
    
####################################################
#
# Add User
#
####################################################

@app.route('/api/create-user', methods=['POST'])
def create_user() -> Response:
    app.logger.info('Adding new user')

    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if User.query.filter_by(username=username).first():
            return make_response(jsonify({'error': 'Invalid username, username already taken'}), 400)
        User.create_user(username, password)
        return make_response(jsonify({'status': 'success', 'username': username}), 200)
    except:
        return make_response(jsonify({"error": "An error occurred while creating the user"}), 500)

@app.route('/api/remove-user', methods=['DELETE'])
def remove_user() -> Response:
    app.logger.info('Deleting current user')

    try:
        data = request.get_json()
        username = data.get('username')
        if not User.query.filter_by(username=username).first():
            return make_response(jsonify({'error': 'Invalid username, user does not exist'}), 400)
        User.delete_user(username)
        return make_response(jsonify({'status': 'success', 'username': username}), 200)
    except:
        return make_response(jsonify({"error": "An error occurred while deleting the user"}), 500)

@app.route('/api/change-password', methods=['POST'])
def change_password() -> Response:
    app.logger.info('Changing user password')

    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if not User.query.filter_by(username=username).first():
            return make_response(jsonify({'error': 'Invalid username, user does not exist'}), 400)
        User.update_password(username, password)
        return make_response(jsonify({'status': 'success', 'username': username}), 200)
    except:
        return make_response(jsonify({"error": "An error occurred while updating the password"}), 500)

@app.route('/api/login', methods=['POST'])
def login():
    """
    Route to log in a user.

    Expected JSON Input:
        - username (str): The username of the user.
        - password (str): The user's password.

    Returns:
        JSON response indicating the success of the login.

    Raises:
        400 error if input validation fails.
        401 error if authentication fails (invalid username or password).
        500 error for any unexpected server-side issues.
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        app.logger.error("Invalid request payload for login.")
        raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

    username = data['username']
    password = data['password']

    try:
        # Validate user credentials
        if not User.check_password(username, password):
            app.logger.warning("Login failed for username: %s", username)
            raise Unauthorized("Invalid username or password.")

        app.logger.info("User %s logged in successfully.", username)
        return jsonify({"message": f"User {username} logged in successfully."}), 200

    except Unauthorized as e:
        return jsonify({"error": str(e)}), 401
    except Exception as e:
        app.logger.error("Error during login for username %s: %s", username, str(e))
        return jsonify({"error": "An unexpected error occurred."}), 500


####################################################
#
# Favorites Manager
#
####################################################

@app.route('/api/add-favorite', methods=['POST'])
def add_favorite() -> Response:
    """
    Route to add a new location to the favorites dictionary.

    Expected JSON Input:
        - location (str): the location whose weather will be retrieved.

    Returns:
        JSON response indicating the success of the location addition.
    Raises:
        400 error if input validation fails.
        500 error if there is an issue adding the location to favorites.
    """
    app.logger.info('Adding a location to favorites')

    try:
        data = request.get_json()
        location = data.get('location')
        
        if not location:
            return make_response(jsonify({'error': 'Invalid input, all fields are required with valid values'}), 400)

        # Check that location is a string
        try:
            location = str(location)
        except ValueError as e:
            return make_response(jsonify({'error': 'Location must be a string'}), 400)

        # Call the get_weather function to call the api and retrieve the weather
        app.logger.info('Getting weather for %s', location)
        temp, wind, precipitation, humidity = favorites_manager.get_weather(location)

        # Call the add_favorites function to add the location and its current weather to the favorites dictionary
        app.logger.info('Adding location and weather to favorites')
        favorites_manager.add_favorite(location, temp, wind, precipitation, humidity)

        app.logger.info("Location added: %s", location)
        return make_response(jsonify({'status': 'success', 'location': location}), 200)
    
    except Exception as e:
        app.logger.error("Failed to add favorite: %s", str(e))
        return make_response(jsonify({'error': str(e)}), 500)
