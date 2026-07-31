"""
Data Layer (Section 2.4 in Report):
Handles direct database read/write queries.
Isolates SQL/Database mechanisms from Business Logic Layer.
"""

from typing import Optional, Dict, Any
from datetime import datetime, timezone
from app.db.database import db_instance, InMemoryDatabase

class UserRepository:
    def __init__(self, db: InMemoryDatabase = db_instance):
        self.db = db

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user by username from Data Layer.
        Directly aligns with Page 7 in Report: get_user_by_username(username)
        """
        for user in self.db.users.values():
            if user["username"].lower() == username.lower():
                return user
        return None

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Retrieve user by email address."""
        for user in self.db.users.values():
            if user["email"].lower() == email.lower():
                return user
        return None

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve user by primary key ID."""
        return self.db.users.get(user_id)

    def save_user(self, username: str, email: str, full_name: str, hashed_password: str) -> Dict[str, Any]:
        """Insert and save new user record in Data Layer."""
        user_id = self.db.get_next_id()
        user_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name,
            "hashed_password": hashed_password,
            "is_active": True,
            "created_at": datetime.now(timezone.utc)
        }
        self.db.users[user_id] = user_data
        return user_data
