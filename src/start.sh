#!/bin/bash
/mongodb/bin/mongod --fork --logpath /mongodb/log/mongod.log --dbpath /mongodb/db
python3 app.py