from flask import Flask, request
from db import Repository
import os
from dotenv import load_dotenv
from assistant import Assistant
from celery_config import create_celery_app

load_dotenv()

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@rabbitmq//',  # Updated to use the Docker Compose service name for RabbitMQ
    CELERY_RESULT_BACKEND='rpc://'
)
celery = create_celery_app(app)
assistant = Assistant(os.getenv('OPENAI_API_KEY'), os.getenv('ASSISTANT_ID'), db)

import tasks  # Import tasks


# Use the Docker Compose service name 'mongodb' as the host
db = Repository("mongodb://mongodb:27017/")  

@app.route('/')
def home():
    return "Hello world"

@app.route('/user/new', methods = ['POST'])
def new_user():
    if request.method == 'POST':
        dataform = request.get_json()
        if not "email" in dataform:
            return "Missing email", 403
        email = dataform['email']
        if not "name" in dataform:
            return "Missing name", 403
        name = dataform['name']

        user = assistant.create_user(email, name)
        if user == None:
            return "User already exists", 403
        else:
            return "User was created with success."
    else:
        return "", 405

@app.route('/user/status', methods = ['GET', 'POST'])
def user_status():

    if request.method == 'POST':
        dataform = request.get_json()
        if not "email" in dataform:
            return "Missing email", 403
        email = dataform['email']
        if not "status" in dataform:
            return "Missing status", 403
        status = dataform['status']

        user = db.get_user(email)
        if user == None:
            return "Not fount", 404
        db.set_status(user, status)
        return status
        
    elif request.method == 'GET':
        email = request.args.get('email', default = "", type = str)
        user = db.get_user(email)
        if user == None:
            return "Not found", 404
        return str(user["status"])

    else:
        return "", 405

@app.route('/user/exists')
def user_exists():
    email = request.args.get('email', default = "", type = str)
    if not db.user_exists(email):
        return "Not found", 404
    return email

@app.route('/test')
def test():
    msgs = assistant.get_reply("bob@gmail.com", "Getting home soon", "Hey bob, how are you doing? Cheers, Johnny", "john@gmail.com", "bob@gmail.com")
    print(msgs)
    return "OK"

@app.route('/add/<int:x>/<int:y>')
def add_task(x, y):
    result = tasks.add.delay(x, y)
    return f"Task enqueued, ID: {result.id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)