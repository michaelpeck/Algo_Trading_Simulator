import datetime as dt
from src.common.database import Database
from urllib.request import Request, urlopen


class Submission(object):
    def __init__(self, ticker, start, end, money):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.money = money

    @staticmethod
    def verify_date(date):
        try:
            dt.datetime.strptime(date, '%m/%d/%Y')
        except ValueError:
            return False
        return True

    @staticmethod
    def verify_ticker(ticker):
        ticker = ticker.upper()
        url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=%s' % (ticker, 'n')
        with urlopen(Request(url)) as response:
            content = response.read().decode().strip().strip('"')
        return content != 'N/A'

    @staticmethod
    def verify_money(money):
        try:
            val = int(money)
            if val < 0:
                return False
            break
        except ValueError:
            return False
        return True
