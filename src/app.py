from flask import Flask
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
users = db["users"]

@app.route('/')
def home():
    mydict = { "name": "John", "address": "Highway 37" }
    x = users.insert_one(mydict)
    return str(x.inserted_id)


app.run(host='0.0.0.0', port=8080)
