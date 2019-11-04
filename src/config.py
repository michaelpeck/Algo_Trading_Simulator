__author__ = 'michaelpeck'

import os

class Config:
    SECRET_KEY = 'ebe982043bc2960b20d1a518ea8112dc'
    URI = "mongodb://localhost:27017/sensedb"
    DATABASE = 'AlgoTrading'
    MONGODB_SETTINGS = {
        'db': 'sensedb',
        'host': "mongodb://localhost:27017/sensedb"
    }
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sensebotco@gmail.com'
    MAIL_PASSWORD = 'BigTime$$'