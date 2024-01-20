from flask import Flask
from flask import request
from db import Repository
from celery_config import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='pyamqp://guest@rabbitmq//',  # Updated to use the Docker Compose service name for RabbitMQ
    CELERY_RESULT_BACKEND='rpc://'
)
celery = make_celery(app)

# Use the Docker Compose service name 'mongodb' as the host
db = Repository("mongodb://mongodb:27017/")  

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)





