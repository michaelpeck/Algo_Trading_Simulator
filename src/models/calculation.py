import datetime as dt
import yfinance as yf
import pandas as pd

class Calculation(object):
    def __init__(self, ticker, start, end, money, trade_point):
        self.ticker = upper(ticker)
        self.start = start
        self.end = end
        self.money = money
        self.tp = trade_point

    @staticmethod
    def algo(self):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period="1mo", interval="2m")
        owned = 0
        count = 0
        for index, row in df.iterrows():
            count += 1
            if money > 0 and row['Low'] < self.tp:
                value = ((row['Low']*row['Volume'])/5)
                if value>money>0:
                    owned += (money/row['Low'])
                    money = 0
                elif money>value>0:
                    owned += (value/row['Low'])
                    money -= value
            if owned > 0 and row['High'] > self.tp:
                halfvol = row['Volume']/2
                if halfvol > owned:
                    money += (owned*row['High'])
                    owned = 0
                elif owned > halfvol:
                    money += (halfvol*row['High'])
                    owned -= halfvol

        if owned > 0:
            money += df.Low.ix[count-1]*owned
            owned = 0

        return money
