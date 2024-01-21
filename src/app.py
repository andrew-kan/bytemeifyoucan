from flask import Flask, request, jsonify
from db import Repository
import os
from dotenv import load_dotenv
from assistant import Assistant
from celery_config import create_celery_app
from bson.json_util import dumps
from db import Repository
from flask_cors import CORS



db = Repository(flush_db=False)

load_dotenv()

# Use the Docker Compose service name 'mongodb' as the host
# db = Repository("mongodb://mongodb:27017/", flush_db=False)  

app = Flask(__name__)
CORS(app)
app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@rabbitmq//',  # Updated to use the Docker Compose service name for RabbitMQ
    CELERY_RESULT_BACKEND='rpc://'
)
celery = create_celery_app(app)
# assistant = Assistant(os.getenv('OPENAI_API_KEY'), os.getenv('ASSISTANT_ID'), db)

import tasks  # Import tasks

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

        user = tasks.create_user.delay(email, name)
        print(user)
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

        if not tasks.set_user_status.delay(email, status):
            return "Not found", 404
        return status
        
    elif request.method == 'GET':
        email = request.args.get('email', default = "", type = str)
        status = tasks.get_user_status(email)
        if status == None:
            return "Not found", 404
        return status

    else:
        return "", 405

@app.route('/user/exists', methods=['GET'])
def user_exists():
    email = request.args.get('email', default = "", type = str)
    if not tasks.user_exists.delay(email):
        return "Not found", 404
    return email

@app.route('/email', methods=['GET'])
def get_emails():
    email = request.args.get('email', default = "", type = str)
    status = request.args.get('status', default = "pending", type = str)
    res = tasks.get_emails(email, status)
    return dumps(res)


@app.route('/api/getallemails', methods=['GET'])
def get_all_emails():
    emails = db.get_all_email()
    to_return  = []
    #skipping content because at this time encoding is weird in my version of the db.
    for email in emails:
        to_return.append({"subject":email["Subject"], "from":email["From"], "content":"MOCK CONTENT", "reply":"I love it", "option1":"Yes", "option2":"no", "category":"sussy"})

    return jsonify(to_return)
    


# @app.route('/reply', methods=['POST'])
# def reply():
#     dataform = request.get_json()
#     if not "email" in dataform:
#         return "Missing email", 403
#     email = dataform["email"]
#     if not "from" in dataform:
#         return "Missing origin person email", 

#     user = db.get_user(email)
#     if user == None:
#         return "Not found", 404
    
#     res = assistant.get_reply(email, user["status"], "Hey bob, how are you doing? Cheers, Johnny", "john@gmail.com", "bob@gmail.com")
#     print(msgs)
#     return "OK"

# @app.route('/add/<int:x>/<int:y>')
# def add_task(x, y):
#     result = tasks.add.delay(x, y)
#     return f"Task enqueued, ID: {result.id}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)