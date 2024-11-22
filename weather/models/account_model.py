from hashlib import sha256
import random
import string

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

def create_user(username: str, password: str) -> None:
    """
    Create a new user by adding it to the users table in the database.

    Args:
        username (str): The user's chosen username
        password (str): The user's chosen password

    Raises:
        ValueError: If the username is invalid.
        ValueError: If a user with the same username already exists
        sqlite3.Error: If any other database error occurs.
    """
    if not isinstance(username, (str)):
        raise ValueError(f"Invalid username: {username}. Username must be a string.")

    salt = ''.join(random.choices(string.ascii_letters, k=2))
    salted_pass = password + salt
    password_hash = sha256(salted_pass.encode('UTF-8').hexdigest())

    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user, password_hash, salt)
                VALUES (?, ?, ?)
            """, (username, password_hash, salt))
            conn.commit()

            logger.info("Meal successfully added to the database: %s", username)

    except sqlite3.IntegrityError:
        logger.error("Duplicate username: %s", username)
        raise ValueError(f"Username with '{username}' already exists")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def login(entered_username: str, password: str) -> str:
    """
    Logs a user in with their username and password.

    Args:
        username (str): The user's username.
        password (str): The user's plaintext password.

    Raises:
        sqlite3.Error: If there's a database error.
        ValueError: If the account with the given username is not found or is deleted.
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password_hash, salt, deleted FROM users WHERE username = ?", (entered_username,))
            row = cursor.fetchone()

            if row:
                if row[4]:
                    logger.info("Account with username %s has been deleted", entered_username)
                    raise ValueError(f"Account with username {entered_username} has been deleted")
                user = User(id=row[0], username=row[1], password_hash=row[2], salt=row[3])
                password += user.salt
                entered_hashed_pass = sha256(password.encode('UTF-8').hexdigest())
                if entered_username == user.username and entered_hashed_pass == user.password_hash:
                    return "Login Successful!"
                else:
                    return "Sorry, incorrect username or password"
            else:
                logger.info("Account with username %s not found", entered_username)
                raise ValueError(f"Account with username {entered_username} not found")

    except sqlite3.Error as e:
        logger.error("Database error: %s", str(e))
        raise e

def update_password() -> None:
    pass