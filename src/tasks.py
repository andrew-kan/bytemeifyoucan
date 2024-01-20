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
def process_email(from_address, subject, content, timestamp):
    # Store the email in MongoDB
    email_id = emails_collection.insert_one({
        "from": from_address,
        "subject": subject,
        "content": content,
        "timestamp": timestamp
    }).inserted_id

    # Call ChatGPT API
    response = requests.post(
        None,
        headers={'Authorization': f'Bearer {None}'},
        json={"prompt": content}
    )

    if response.status_code == 200:
        # Get reply from GPT
        gpt_reply = response.json()

        # Store reply to the DB
        emails_collection.update_one(
            {"_id": ObjectId(email_id)},
            {"$set": {"gpt_reply": gpt_reply}}
        )
    else:
        # Handle error or API failure
        print("Failed to get response from ChatGPT API")

    return email_id  # or return some meaningful result
