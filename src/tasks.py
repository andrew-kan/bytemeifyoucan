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
    user = assistant.create_user(email, name)
    if user == None:
        return None
    else:
        return str(user)

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
def process_email(recv_email, email_owner):
    if not db.user_exists(email_owner):
        return None
    print(recv_email["Content"])
    msgs = recv_email["Content"][0].split(b'\xe2\x80\xaf')
    for i in range(len(msgs)):
        if isinstance(msgs[i], bytes):
            msgs[i] = msgs[i].decode('utf-8', errors="replace")
    replies = assistant.get_reply(email_owner, recv_email["Subject"], "".join(msgs[0:min(len(msgs), 2)]), recv_email["From"], recv_email["To"])
    
    # if reply["spam"]:
    #     print("Spam detected, no reply returned")
    #     db.create_email(email_owner, "scam", recv_email, "")
    # else:
    db.create_email(email_owner, "pending", recv_email, replies)

    return str(replies)

@celery.task
def get_emails(email, status):
    return db.get_emails(email, status)

# @celery.task
# def update_email():
#     # regen reply
#     # update to database
#     return

# @celery.task
# def accept_email()
#     # send email
#     # update to database
#     return

# @celery.task
# def deny_email()
#     # update to database
#     return