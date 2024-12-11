#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done


###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed h."
    exit 1
  fi
}

# Function to check the health of the service
check_db() {
  echo "Checking database status..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed db."
    exit 1
  fi
}

##############################################
#
# User management
#
##############################################

# Function to create a user
create_user() {
  username=$1
  password=$2

  echo "Creating a new user with username $username"
  curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}" | grep -q "status": "user added"
  if [ $? -eq 0 ]; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to log in a user
login_user() {
  username=$1
  password=$2
  echo "Logging in user..."
  response=$(curl -s -X POST "$BASE_URL/login" -H "Content-Type: application/json" \
    -d "{"username":\"$username\", "password":\"$password\"}")
  if echo "$response" | grep -q '"message": "User testuser logged in successfully."'; then
    echo "User logged in successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Login Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log in user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to log out a user
logout_user() {
  username=$1

  echo "Logging out user..."
  response=$(curl -s -X POST "$BASE_URL/logout" -H "Content-Type: application/json" \
    -d '{"username":"testuser"}')
  if echo "$response" | grep -q ""message": "User \"$username\" logged out successfully.""; then
    echo "User logged out successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Logout Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to log out user."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error Response JSON:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

##############################################
#
# Favorites Manager
#
##############################################

add_favorite() {
  location=$1

  echo "Adding a favorite..."
  curl -s -X POST "$BASE_URL/add-favorite" -H "Content-Type: application/json" \
    -d "{"location":\"$Location\"}" | grep -q '"status": "success"'
  if [ $? -eq 0 ]; then
    echo "Location added successfully."
  else
    echo "Failed to add location."
    exit 1
  fi
}

get_favorite_weather() {
  location=$1

  echo "Getting weather from a favorite location: ($location)..."
  response=$(curl -s -X GET "$BASE_URL/get-favorite-weather/$location")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Weather for ($location) retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Weather JSON (Favorite Location $location):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get weather for favorite location ($location)."
    exit 1
  fi
}

get_all_favorites_current_weather() {
  echo "Getting all favorite locations..."
  response=$(curl -s -X GET "$BASE_URL/get-all-favorites-current-weather")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All favorites with their weather retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Favorites weather JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get all favorites weather."
    exit 1
  fi
}

get_favorite_historical() {
  location=$1

  echo "Getting historical weather from a favorite location: ($location)..."
  response=$(curl -s -X GET "$BASE_URL/get-favorite-historical-weather/$location")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Historical weather for ($location) retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Historical Weather JSON (Favorite Location $location):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get historical weather for favorite location ($location)."
    exit 1
  fi
}

get_favorite_forecast() {
  location=$1

  echo "Getting next day forecast for a favorite location: ($location)..."
  response=$(curl -s -X GET "$BASE_URL/get-favorite-forecast/$location")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Forecast for ($location) retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Forecast JSON (Favorite Location $location):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get forecast for favorite location ($location)."
    exit 1
  fi
}

clear_favorites() {
  echo "Clearing favorites..."
  curl -s -X DELETE "$BASE_URL/clear-favorites" | grep -q '"status": "success"'
}

get_all_favorites() {
  echo "Getting all favorite locations..."
  response=$(curl -s -X GET "$BASE_URL/get-all-favorites")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "All favorite locations retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Favorites JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get all favorites."
    exit 1
  fi
}

get_favorite_alerts() {
  location=$1

  echo "Getting alerts from a favorite location: ($location)..."
  response=$(curl -s -X GET "$BASE_URL/get-favorite-alerts/$location")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Alerts for ($location) retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Alerts JSON (Favorite Location $location):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get alerts for favorite location ($location)."
    exit 1
  fi
}

get_favorite_coordinates() {
  location=$1

  echo "Getting historical weather from a favorite location: ($location)..."
  response=$(curl -s -X GET "$BASE_URL/get-favorite-coordinates/$location")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Coordinates for ($location) retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Coordinates JSON (Favorite Location $location):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get alerts for favorite location ($location)."
    exit 1
  fi
}

check_health
check_db
create_user abc 123
login_user abc 123
logout_user abc
add_favorite boston
get_favorite_weather boston
get_all_favorites_current_weather
get_favorite_historical boston
get_favorite_forecast boston
get_all_favorites
clear_favorites
add_favorite london
get_all_favorites
get_favorite_alerts london
get_favorite_coordinates london
get_all_favorites