from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from sqlalchemy.sql import text
import sqlite3
from db import db
import requests
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("API_KEY")
weather_api = "http://api.weatherapi.com/v1"

# Initialize SQLLite SQLAlchemy DB through Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from weather.models.account_model import User
#from weather.models.favorites_manager import FavoritesManager

#favorites_manager = FavoritesManager()


with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e)
        
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

@app.route('/api/add-user', methods=['POST'])
def add_user() -> Response:
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
    