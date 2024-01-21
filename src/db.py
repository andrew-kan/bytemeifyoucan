import pymongo

class Repository():
    def __init__(self, path="mongodb://mongodb:27017/", db_name="mydatabase", flush_db=True):
        self.client = pymongo.MongoClient(path)

        # Init database
        if db_name in self.client.list_database_names() and flush_db:
            self.client.drop_database(db_name)
        self.db = self.client[db_name]

        # Tables
        self.users = self.db["Users"]
        self.users.create_index("email", unique=True)

        self.emails = self.db["Emails"]

    def create_user(self, name, email, thread_id):
        try:
            return self.users.insert_one({"name": name, 
                                            "email": email, 
                                            "thread": thread_id,
                                            "status": ""
                                        })
        except pymongo.errors.DuplicateKeyError:
            return None

    def user_exists(self, email):
        return self.users.find_one({ "email": email }) != None

    def get_user(self, email):
        return self.users.find_one({ "email": email })

    def set_user_status(self, user, status):
        self.users.update_one(user, { "$set": { "status": status } })
    
    def create_email(self, owner, status, recv_email, reply):
        try:
            return self.emails.insert_one({"owner": owner, 
                                            "status": status, 
                                            "email": recv_email,
                                            "reply": reply
                                        })
        except Exception as e:
            print(f"Error happened: {e}")
            return None
    
    def get_emails(self, owner, status):
        return self.emails.find({"owner": owner, "status": status})

    