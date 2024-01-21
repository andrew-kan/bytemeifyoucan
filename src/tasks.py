from app import celery
import pymongo
import requests
from bson import ObjectId
from db import Repository


# Setup MongoDB connection
client = pymongo.MongoClient("mongodb://mongodb:27017/")
db = client["mydatabase"]
emails_collection = db.emails

@celery.task
def add(x, y):
    return x + y

@celery.task
def process_email(email_obj):

    emails_collection.insert_one(email_obj)
    
    return "pushed email"  # or return some meaningful result
