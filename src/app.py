from flask import Flask, request, jsonify
from db import Repository
import os
from dotenv import load_dotenv
from assistant import Assistant
from celery_config import create_celery_app
from bson.json_util import dumps
from db import Repository
from flask_cors import CORS
import sendmail
from bson import ObjectId
from sendmail import reply_to_email


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

@app.route('/api/user/new', methods = ['POST'])
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

@app.route('/api/user/status', methods = ['GET', 'POST'])
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

@app.route('/api/user/exists', methods=['GET'])
def user_exists():
    email = request.args.get('email', default = "", type = str)
    if not tasks.user_exists.delay(email):
        return "Not found", 404
    return email

@app.route('/api/email', methods=['GET'])
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
    # for email in emails:
       # to_return.append({"subject":email["Subject"], "category":email.get("cateogry", "important") "from":email["From"], "content":"It is also no secret that I have not been happy with your approach to how you manage me as an employee, and therefore I am formally requesting that you relinquish control of the inventory team to a manager who is able to be on the floor more often and can see what is actually going on, and can see the impact of the workload on each individual in the department on a daily basis and does not need to rely on other people telling you about what is going on in your department. There are job duties that I had done for months before [M - already gone] had started that you have told me I will need to be trained on once things settle down a little, which tells me that you do not really even know what I do/have done while working under you. As we have already discussed, I do not think that it is right that my job role has been changed every few months with no prior discussion beforehand, and no discussion on pay increase with the added responsibility. You have once again basically done the same thing when I asked you if production orders would be a permanent part of my job duties and you told me no, then casually put in an email shortly after that it is a part of my permanent duties now. I do not wish for you to feel personally attacked as you seem like a nice person, and I understood you do a lot at work, but perhaps looking after inventory is too much on top of everything else you do. However, at the end of the day, I do not feel I can continue working under you as my manager, I do not wish to leave the company, but if it comes down to it, I will not continue to work at a place where I am this unhappy and feel like I am getting screwed over and disrespected. I do enjoy the job and am hoping to have a long career within [company] so long as this can get settled."
    #,# "reply":"I love it", "option1":"Yes", "option2":"no", "category":"sussy"})

    return jsonify(to_return)
    


@app.route('/api/reply', methods=['POST'])
def reply():
    dataform = request.get_json()

    email_object = dataform["email"]
    replymsg = dataform["replymsg"]


    # original needs to contain messageid, from, subject
    # sendmail.reply_to_email(dataform["original"], dataform["replymsg"])
    reply_to_email(email_object, replymsg)
    
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