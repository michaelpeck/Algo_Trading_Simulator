__author__ = 'michaelpeck'

import uuid
import datetime as dt
from src.common.database import Database
from src import db
from flask_login import UserMixin


TYPES = (('SR', 'Static Range'),
         ('MA', 'Moving Average'),
         ('WMA', 'Weighted Moving Average'))

class Model(UserMixin, db.Document):
    meta = {'collection': 'models'}
    name = db.StringField(max_length=30)
    mod_type = db.StringField(max_length=3, choices=TYPES)
    ticker = db.StringField(max_length=6)
    period = db.StringField(max_length=6)
    interval = db.StringField(max_length=6)
    money = db.FloatField()
    buy = db.FloatField()
    sell = db.FloatField()
    av_length = db.IntField()
    trade_cost = db.FloatField()
    owner = db.LazyReferenceField('User')

