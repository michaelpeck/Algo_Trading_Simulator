__author__ = 'michaelpeck'

import uuid
import datetime as dt
from src.common.database import Database

class Model(object):
    def __init__(self, ticker, period, interval, money, buy, sell, trade_cost, name=None, user_id=None, _id=None):
        self.ticker = ticker
        self.period = period
        self.interval = interval
        self.money = money
        self.buy = buy
        self.sell = sell
        self.trade_cost = trade_cost
        self.name = "" if name is None else name
        self._id = uuid.uuid4().hex if _id is None else _id
        self.user_id = user_id

    @classmethod
    def create_model(cls, ticker, period, interval, money, buy, sell, trade_cost, name, user_id):
        new_model = cls(ticker, period, interval, money, buy, sell, trade_cost, name, user_id)
        new_model.save_to_mongo()
        return new_model._id

    def save_to_mongo(self):
        Database.insert(collection='models', data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'user_id': self.user_id,
            'name': self.name,
            'ticker': self.ticker,
            'money': self.money,
            'period': self.period,
            'interval': self.interval,
            'buy': self.buy,
            'sell': self.sell,
            'trade_cost': self.trade_cost
        }

    @classmethod
    def from_mongo(cls, id):
        model = Database.find_one(collection='models',
                                   query={'_id': id})
        return cls(**model)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("models", {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_id_by_name(cls, name):
        data = Database.find_one("models", {"name": name})
        if data is not None:
            return data['_id']

    @classmethod
    def find_by_user_id(cls, user_id):
        models = Database.find(collection='models',
                                query={'user_id': user_id})
        return [cls(**model) for model in models]