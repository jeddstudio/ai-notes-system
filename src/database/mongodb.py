import os
from pymongo import MongoClient
from dotenv import load_dotenv

# take environment variables from .env
load_dotenv()

def init_db():
    client = MongoClient(os.getenv('MONGODB_URL'))
    db = client.ai_notes_db
    return db

def get_db():
    db = init_db()
    try:
        yield db
    finally: # Close when done
        db.client.close()
