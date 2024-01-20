from flask import Flask
from flask import request
from db import Repository

app = Flask(__name__)
db = Repository("mongodb://localhost:27017/")

@app.route('/')
def home():
    return "Hello world"

@app.route('/user/new')
def new_user():
    user = db.create_user("John doe", "johndoe@gmail.com")
    if user == None:
        return "User already exists", 403
    else:
        print(user)
        return f"User was created with success."

@app.route('/user/exists')
def user_exists():
    email = request.args.get('email', default = "", type = str)
    if not db.user_exists(email):
        return "Not found", 404
    return email

app.run(host='0.0.0.0', port=8080)
