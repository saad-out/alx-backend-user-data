#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash password using bcrypt
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate new UUID
    """
    return str(uuid.uuid4())


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

    def create_session(self, email: str) -> str:
        """Create session ID for user
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user_id=user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get user by session ID
        """
        if session_id is None:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
