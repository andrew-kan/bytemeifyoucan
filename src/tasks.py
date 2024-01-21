from app import celery
import requests
from bson import ObjectId
from db import Repository
from assistant import Assistant
from dotenv import load_dotenv
import os

load_dotenv()

# Setup MongoDB connection
db = Repository("mongodb://mongodb:27017/", flush_db=False) 
assistant = Assistant(os.getenv('OPENAI_API_KEY'), os.getenv('ASSISTANT_ID'), db)

@celery.task
def create_user(email, name):
    return assistant.create_user(email, name)

@celery.task
def set_user_status(email, status):
    user = db.get_user(email)
    if user == None:
        return False
    db.set_user_status(user, status)
    return True

@celery.task
def get_user_status(email):
    user = db.get_user(email)
    if user == None:
        return None
    return str(user["status"])

@celery.task
def user_exists(email):
    return db.user_exists(email)
    

@celery.task
def process_email(email_obj):

    print(email_obj["Content"])


    # emails_collection.insert_one(email_obj)
    
    return "pushed email"  # or return some meaningful result
