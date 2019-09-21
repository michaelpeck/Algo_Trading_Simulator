import uuid
import datetime as dt
import yfinance as yf
import pandas as pd
from src.common.database import Database

class Calculation(object):
    def __init__(self, ticker, period, interval, money, buy, sell, _id=None):
        self.ticker = upper(ticker)
        self.period = period
        self.interval = interval
        self.money = money
        self.buy = buy
        self.sell = sell
        self._id = uuid.uuid4().hex if _id is None else _id
        self.final_money = 0

    @staticmethod
    def algo(ticker, period, interval, money, buy, sell, _id):
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trade_money = float(money)
        buy = float(buy)
        sell = float(sell)
        for index, row in df.iterrows():
            count += 1
            if trade_money > 0 and row['Low'] <= buy:
                value = ((row['Low']*row['Volume'])/5)
                if value>trade_money>0:
                    owned += (trade_money/row['Low'])
                    trade_money = 0
                elif trade_money>value>0:
                    owned += (value/row['Low'])
                    trade_money -= value
            if owned > 0 and row['High'] >= sell:
                halfvol = row['Volume']/2
                if halfvol > owned:
                    trade_money += (owned*row['High'])
                    owned = 0
                elif owned > halfvol:
                    trade_money += (halfvol*row['High'])
                    owned -= halfvol

        if owned > 0:
            trade_money += df.Low.ix[count-1]*owned
        return [ticker, period, interval, money, buy, sell,trade_money _id]

    @classmethod
    def log_final_money(cls, trade_money, id):
        transaction = cls.get_by_id(id)
        transaction.final_money = trade_money

    def save_to_mongo(self):
        Database.insert(collection='entries', data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'ticker': self.ticker,
            'starting_balance': self.money,
            'ending_balance': self.final_money,
            'period': self.period,
            'interval': self.interval,
            'buy': self.buy,
            'sell': self.sell
        }

    @classmethod
    def from_mongo(cls, id):
        entry_data = Database.find(collection='entries',
                                   query={'entry_id': id})
        return cls(**entry_data)

    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("entries", {"_id": _id})
        if data is not None:
            return cls(**data)