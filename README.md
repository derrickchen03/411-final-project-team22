# 411-final-project-team22

## Project Description
DESCRIPTION

### Route Documentation

Route: /add-favorite

Request Type: POST

Purpose: Adds a favorite to the user's list of favorites

Request Body:
'''
    user_id (Integer): The ID for the user currently logged in.
    location (String): The location to be added to the favorites.
'''
Response Format: JSON
    Success Response:
Example Request:
Example Response:

Route: /clear-favorites/<int:user_id>
Request Type: DELETE
Purpose: Clear the dictionary of the user's favorite weather locations.
Request Body:
    user_id (Integer): The ID for the user currently logged in.
Response Format: JSON
    Success Response Example:
        Code: 200
        Content: {"status": "success"}
Example Request:
Example Response:
