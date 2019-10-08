import pymongo


class Database(object):
    URI = "mongodb+srv://algo_trader:testpass@cluster0-zpslf.mongodb.net/test?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
    db = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb+srv://algo_trader:testpass@cluster0-zpslf.mongodb.net/test?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
        Database.db = client.get_database('AlgoTrading')

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.db[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.db[collection].find_one(query)

    @staticmethod
    def find_all(collection):
        return Database.db[collection].find()