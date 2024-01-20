import pymongo

class Repository():
    def __init__(self, path="mongodb://localhost:27017/", db_name="mydatabase", flush_db=True):
        self.client = pymongo.MongoClient(path)

        # Init database
        if db_name in self.client.list_database_names() and flush_db:
            self.client.drop_database(db_name)
        self.db = self.client[db_name]

        # Tables
        self.users = self.db["users"]
        self.users.create_index("email", unique=True)

    def create_user(self, name, email):
        try:
            return self.users.insert_one({"name": name, "email": email})
        except pymongo.errors.DuplicateKeyError:
            return None

    def user_exists(self, email):
        return self.users.find_one({ "email": email }) != None

    