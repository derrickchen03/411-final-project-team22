import logging
from typing import Any, List

from clients.mongo_client import sessions_collection
from utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class MongoSessionModel:

    @staticmethod
    def login_user(user_id: int, favorites: dict) -> None:
        """
        Load the user's favorites from MongoDB into the FavoritesManager's favorites dictionary.

        Checks if a session document exists for the given `user_id` in MongoDB.
        If it exists, clears any current favorites and loads
        the stored favorites from MongoDB into the favorites dictionary.

        If no session is found, it creates a new session document for the user
        with an empty favorites list in MongoDB.

        Args:
            user_id (int): The ID of the user whose session is to be loaded.
            favorites (dict): A dictionary of favorites where the user's favorites
            will be loaded.
        """
        session = sessions_collection.find_one({"user_id": user_id})
        if session:
            # Clear any previous favorites in the model
            favorites.clear()
            for favorite in session.get("favorites", {}):
                favorite.get_favorite_weather()
                pass
        else:
            sessions_collection.insert_one({"user_id": user_id, "favorites": {}})

    @staticmethod
    def logout_user(user_id: int, favorites: dict) -> None:
        """
        Store the current favorites from the favorites dictionary back into MongoDB.

        Retrieves the current favorites from 'favorites' and attempts to store them in
        the MongoDB session document associated with the given 'user_id'. If no session
        document exists for the user, raises a 'ValueError'.

        After saving the favorites to MongoDB, the favorites dictionary is
        cleared to ensure a fresh state for the next login.

        Args:
            user_id (int): The ID of the user whose session data is to be saved.
            favorites (dict): A dictionary of the weather in the user's favorite locations.

        Raises:
            ValueError: If no session document is found for the user in MongoDB.
        """
        result = sessions_collection.update_one(
            {"user_id": user_id},
            {"$set": {"favorites": favorites}},
            upsert=False  # Prevents creating a new document if not found
        )

        # Check if a document was actually modified (i.e., user was found)
        if result.matched_count == 0:
            logger.error("User %s not found in MongoDB for logout.", user_id)
            raise ValueError(f"User with ID {user_id} not found for logout.")

        # Clear the combatants from the model after successfully logging out
        favorites.clear()