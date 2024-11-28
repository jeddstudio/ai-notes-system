from datetime import datetime

class NoteProcessor:
    def __init__(self):
        self.db = None
    
    def set_db(self, db):
        self.db = db
    
    # Create a note
    def create_note(self, title: str, content: str):
        note = {
            "title": title,
            "content": content,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        return self.db.notes.insert_one(note)
    
