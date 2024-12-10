# 411-final-project-team22

## Project Description
DESCRIPTION

### Route Documentation
#### User Management 
```
Route: /create-user

Request Type: POST
Purpose: Adds a new user.
Request Body:
    username (str): user's new username
    password (str): user's chosen password
Response Format: JSON
    Success Response:
        Code: 200
        Content: 
Example Request:
Example Response:
```
```
Route: /remove-user

Request Type: DELETES
Purpose: Deletes an existing user.
Request Body:
    username (str): user username which already exists
Response Format: JSON
    Success Response:
        Code: 200
        Content: 
Example Request:
Example Response:
```
```
Route: /change-password

Request Type: POST
Purpose: Changes the password of an existing user.
Request Body:
    username (str): user username which already exists
    password (str): user's chosen new password
Response Format: JSON
    Success Response:
        Code: 200
        Content: 
Example Request:
Example Response:
```
```
Route: /compare-password

Request Type: PUT
Purpose: Compares the username and password that is entered to that which already exists.
Request Body:
    username (str): user username which already exists
    password (str): user's password
Response Format: JSON
    Success Response:
        Code: 200
        Content: 
Example Request:
Example Response:
```
```
Route: /login

Request Type: POST
Purpose: Logins in a user
Request Body:
    username (str): user's username which already exists
    password (str): user's password
Response Format: JSON
    Success Response:
        Code: 200
        Content: {"message": f"User {username} logged in successfully."}
Example Request:
    {
        "username": "newuser",
        "password": "password"
    }
Example Response:
    {
        "message": "User newuser logged in successfully",
        "status": "200"
    }
```
#### Favorites Management
```
Route: /add-favorite

Request Type: POST
Purpose: Adds a favorite to the user's list of favorites
Request Body:
    location (str): The location to be added to the favorites.
Response Format: JSON
    Success Response:
Example Request:
Example Response:
```

```
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
```
