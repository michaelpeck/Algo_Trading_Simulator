import pymongo


class Database(object):
    db = None

    @staticmethod
    def initialize(Config):
        client = pymongo.MongoClient(Config.URI)
        Database.db = client.get_database(Config.DATABASE)

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert(data)

    @staticmethod
    def delete_one(collection, query):
        Database.db[collection].delete_one(query)

    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def find_all(collection):
        return Database.db[collection].find()