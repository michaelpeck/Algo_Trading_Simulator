import yfinance as yf
import numpy as np
import datetime
from src.common.database import Database
from flask_login import current_user, UserMixin
from src import db


class Check(UserMixin, db.Document):
    meta = {'collection': 'checks'}
    ticker = db.StringField()
    name = db.StringField()
    previous_close = db.FloatField()
    three_mo_avg_vol = db.FloatField()
    year_range = db.StringField()



    def get_info(self):
        stock = yf.Ticker(self.ticker)
        info = stock.info
        if info != {}:
            self.name = info['longName']
            self.previous_close = info['regularMarketPreviousClose']
            self.three_mo_avg_vol = info['averageDailyVolume3Month']
            self.year_range = info['fiftyTwoWeekRange']
        self.save()
        return self.id