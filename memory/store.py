import os
import json
from datetime import datetime

class MemoryStore:
    def __init__(self, db_path="memory_db.json"):
        self.db_path = db_path
        self._ensure_db()

    def _ensure_db(self):
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump({}, f)

    def save_execution(self, ticket_id: str, data: dict):
        with open(self.db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        db[ticket_id] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(db, f, indent=4)

    def get_execution(self, ticket_id: str):
        with open(self.db_path, 'r', encoding='utf-8') as f:
            db = json.load(f)
        
        return db.get(ticket_id)
