from hashlib import sha256
import os

from dataclasses import dataclass
import logging
import sqlite3
from typing import Any

from utils.sql_utils import get_db_connection
from utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class User:
    id: int
    username: str
    password_hash: str

def create_meal(username: str, password: str) -> None:
    """
    Create a new user by adding it to the users table in the database.

    Args:
        username (str): The user's chosen username
        password (str): The user's chosen password

    Raises:
        ValueError: If price or difficulty is invalid.
        ValueError: If a meal with the same name already exists (duplicate name).
        sqlite3.Error: If any other database error occurs.
    """
    if not isinstance(username, (str)):
        raise ValueError(f"Invalid username: {price}. Username must be a string.")

    salt = os.urandom(sha256.SALT_SIZE)
    salted_pass = password + salt
    password_hash = sha256(salted_pass.encode('UTF-8').hexdigest())

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user, password_hash, salt)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, salt))
            conn.commit()

            logger.info("Meal successfully added to the database: %s", username)

    except sqlite3.IntegrityError:
        logger.error("Duplicate meal name: %s", meal)
        raise ValueError(f"Meal with name '{meal}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

