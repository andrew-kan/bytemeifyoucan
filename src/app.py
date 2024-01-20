from flask import Flask
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]

@app.route('/')
def home():
    return client.list_database_names()


app.run(host='0.0.0.0', port=8080)
