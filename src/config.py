__author__ = 'michaelpeck'

import os

class Config:
    SECRET_KEY = '2eac05d302d10c2dbce05745a8c0d22a'
    URI = "mongodb+srv://algo_trader:testpass@cluster0-zpslf.mongodb.net/test?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true"
    DATABASE = 'AlgoTrading'
    MONGODB_SETTINGS = {
        'db': 'AlgoTrading',
        'host': 'mongodb+srv://algo_trader:testpass@cluster0-zpslf.mongodb.net/test?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true'
    }
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'sensebotco@gmail.com'
    MAIL_PASSWORD = 'BigTime$$'