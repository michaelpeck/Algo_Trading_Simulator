import uuid
import datetime as dt
import yfinance as yf
import pandas as pd
from src.common.database import Database

class Calculation(object):
    def __init__(self, ticker, period, interval, money, buy, sell, trade_cost, user_id=None, final_money=None, final_volume=None, final_liquid=None, _id=None):
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.money = money
        self.buy = buy
        self.sell = sell
        self.trade_cost = trade_cost
        self.user_id = "guest" if user_id is None else user_id
        self.final_money = 0 if final_money is None else final_money
        self.final_volume = 0 if final_volume is None else final_volume
        self.final_liquid = 0 if final_liquid is None else final_liquid
        self._id = uuid.uuid4().hex if _id is None else _id


    @classmethod
    def algo(cls, ticker, period, interval, money, buy, sell, trade_cost, user_id):
        new_entry = cls(ticker, period, interval, money, buy, sell, trade_cost, user_id)
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trade_money = float(money)
        buy = float(buy)
        sell = float(sell)
        trade_cost = float(trade_cost)
        for index, row in df.iterrows():
            count += 1
            available_money = money - trade_cost
            available_volume = row['Volume']/40
            if available_money > 0 and row['Low'] <= buy:
                value = (row['Low']*available_volume)
                if value>available_money>0:
                    owned += (available_money/row['Low'])
                    trade_money = 0
                elif available_money>value>0:
                    owned += (value/row['Low'])
                    trade_money -= trade_cost
                    trade_money -= value
            if owned > 0 and row['High'] >= sell:
                if available_volume > owned:
                    trade_money += (owned*row['High'])
                    trade_money -= trade_cost
                    owned = 0
                elif owned > available_volume:
                    trade_money += (available_volume*row['High'])
                    trade_money -= trade_cost
                    owned -= available_volume

        if owned > 0:
            liquid_money = trade_money + df.Low.ix[count-1]*owned
        new_entry.final_money = trade_money
        new_entry.final_owned = owned
        new_entry.final_liquid = liquid_money
        new_entry.save_to_mongo()
        return new_entry._id


    def save_to_mongo(self):
        Database.insert(collection='entries', data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'user_id': self.user_id,
            'ticker': self.ticker,
            'money': self.money,
            'final_money': self.final_money,
            'period': self.period,
            'interval': self.interval,
            'buy': self.buy,
            'sell': self.sell
        }

    @classmethod
    def from_mongo(cls, id):
        entry_data = Database.find_one(collection='entries',
                                   query={'_id': id})
        return cls(**entry_data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("entries", {"_id": _id})
        if data is not None:
            return cls(**data)

    @classmethod
    def find_by_user_id(cls, user_id):
        entries = Database.find(collection='entries',
                                query={'user_id': user_id})
        return [cls(**entry) for entry in entries]
