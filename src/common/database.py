import pymongo



class Database(object):
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient("mongodb+srv://algo_trader:atapass123@cluster0-zpslf.mongodb.net/test?retryWrites=true&w=majority")
        Database.DATABASE = client['AlgoTrading']

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
