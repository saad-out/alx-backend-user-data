#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user to database if not exists
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user is not None:
                raise ValueError(f"User {existing_user.email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = User(email=email, hashed_password=hashed_password)
            return self._db.add_user(email, hashed_password.decode("utf-8"))

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password.encode("utf8"))
        except NoResultFound:
            return False
