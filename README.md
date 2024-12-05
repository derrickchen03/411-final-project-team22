# 411-final-project-team22
For CS411 F24 @ BU

Needs to have this at some point:


● What the application does at a high level

● A description of each route (example on ed discussion):

    ○ Route Name and Path
    ○ Request Type
        ■ GET, POST, PUT, DELETE
    ○ Purpose
    ○ Request Format
        ■ GET parameters
        ■ POST / PUT / DELETE body
    ○ Response Format
        ■ JSON keys and value types
    ○ Example
        ■ Request in the form of JSON body or cURL command
        ■ Associated JSON response

Route: /add-favorite
Request Type: POST
Purpose: Adds a favorite to the user's list of favorites
Request Body:
    user_id (Integer): The ID for the user currently logged in.
    location (String): The location to be added to the favorites.
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
