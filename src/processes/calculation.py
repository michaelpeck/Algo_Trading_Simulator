import uuid
import yfinance as yf
import datetime
from src.common.database import Database
from src.processes.models import Model

class Calculation(object):
    def __init__(self, type, ticker, period, interval, money, buy, sell, trade_cost, user_id, date=None, time=None, model_id=None, td=None, tt=None, ty=None, tp=None, tv=None, final_money=None, final_owned=None, final_liquid=None, trades=None, buys=None, sells=None, _id=None):
        self.date = "" if date is None else date
        self.time = "" if date is None else time
        self.type = type
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.money = money
        self.buy = buy
        self.sell = sell
        self.trade_cost = trade_cost
        self.user_id = "guest" if user_id is None else user_id
        self.final_money = 0 if final_money is None else final_money
        self.final_owned = 0 if final_owned is None else final_owned
        self.final_liquid = 0 if final_liquid is None else final_liquid
        self.trades = 0 if trades is None else trades
        self.buys = 0 if buys is None else buys
        self.sells = 0 if sells is None else sells
        self.td = td
        self.tt = tt
        self.ty = ty
        self.tp = tp
        self.tv = tv
        self._id = uuid.uuid4().hex if _id is None else _id
        self.model_id = model_id


    @classmethod
    def static_range(cls, type, ticker, period, interval, money, buy, sell, trade_cost, user_id, date, time, model_id):
        new_entry = cls(type, ticker, period, interval, money, buy, sell, trade_cost, user_id, date, time, model_id)
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trades = 0
        buys = 0
        sells = 0
        trade_money = float(money)
        trade_cost = float(trade_cost)
        buy = float(buy)
        sell = float(sell)
        trade_cost = float(trade_cost)
        td = []     #trade date
        tt = []     #trade time
        ty = []     #trade type
        tp = []     #trade price
        tv = []     #trade volume
        for index, row in df.iterrows():
            count += 1
            available_money = trade_money - trade_cost
            available_volume = row['Volume']/40
            low = round(row['Low'], 4)
            high = round(row['High'], 4)
            date = index.to_pydatetime().strftime("%d-%m-%Y")
            time = index.to_pydatetime().strftime("%H:%M")
            lvalue = (low * available_volume)
            hvalue = (high * available_volume)
            if available_money > 0 and low <= buy and lvalue > trade_cost:
                if lvalue>available_money>0:
                    owned += (available_money/low)
                    trade_money = 0
                    trades += 1
                    buys += 1
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
                elif available_money>lvalue>0:
                    owned += (lvalue/low)
                    trade_money -= trade_cost
                    trade_money -= lvalue
                    trades += 1
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
            if owned > 0 and high >= sell and hvalue > trade_cost:
                if available_volume > owned:
                    trade_money += (owned*high)
                    trade_money -= trade_cost
                    owned = 0
                    trades += 1
                    sells += 1
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
                elif owned > available_volume:
                    trade_money += (available_volume*high)
                    trade_money -= trade_cost
                    owned -= available_volume
                    trades += 1
                    sells += 1
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
        if owned > 0:
            liquid_money = (trade_money - trade_cost) + df.Low.ix[count-1]*owned
        else:
            liquid_money = trade_money

        new_entry.final_money = round(trade_money, 2)
        new_entry.final_owned = round(owned)
        new_entry.final_liquid = round(liquid_money, 2)
        new_entry.trades = trades
        new_entry.buys = buys
        new_entry.sells = sells
        new_entry.td = td
        new_entry.tt = tt
        new_entry.ty = ty
        new_entry.tp = tp
        new_entry.tv = tv
        new_entry.save_to_mongo()
        return new_entry._id


    def save_to_mongo(self):
        Database.insert(collection='entries', data=self.json())


    def json(self):
        return{
            '_id': self._id,
            'user_id': self.user_id,
            'model_id': self.model_id,
            'type': self.type,
            'date': self.date,
            'time': self.time,
            'ticker': self.ticker,
            'money': self.money,
            'final_money': self.final_money,
            'final_owned': self.final_owned,
            'final_liquid': self.final_liquid,
            'trades': self.trades,
            'buys': self.buys,
            'sells': self.sells,
            'td': self.td,
            'tt': self.tt,
            'ty': self.ty,
            'tp': self.tp,
            'tv': self.tv,
            'period': self.period,
            'interval': self.interval,
            'buy': self.buy,
            'sell': self.sell,
            'trade_cost': self.trade_cost
        }

    @classmethod
    def delete_entry_by_id(cls, id):
        Database.delete_one(collection='entries',
                            query={'_id': id})

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
