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

    def algo(self):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period="1mo", interval="2m")
        owned = 0
        count = 0
        trade_money = self.money
        buy = self.buy
        sell = self.sell
        for index, row in df.iterrows():
            count += 1
            if trade_money > 0 and row['Low'] <= buy:
                value = ((row['Low']*row['Volume'])/5)
                if value>trade_money>0:
                    owned += (money/row['Low'])
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
            owned = 0

        self.final_money = trade_money
        self.save_to_mongo()
        return self._id


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