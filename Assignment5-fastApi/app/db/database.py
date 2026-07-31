"""
Data Layer: Database Connection & Store.
Simulates persistence engine (e.g. SQLite / PostgreSQL connection).
"""

from typing import Dict, Any

class InMemoryDatabase:
    def __init__(self):
        self.users: Dict[int, Dict[str, Any]] = {}
        self._id_counter = 1

    def get_next_id(self) -> int:
        current_id = self._id_counter
        self._id_counter += 1
        return current_id

db_instance = InMemoryDatabase()
