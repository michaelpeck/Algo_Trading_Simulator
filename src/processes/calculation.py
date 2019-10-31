import uuid
import yfinance as yf
import numpy as np
import datetime
from src.common.database import Database
from src.processes.models import Model

class Calculation(object):
    def __init__(self, type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp=None, model_id=None, td=None, tt=None, ty=None, tp=None, tv=None, final_money=None, final_owned=None, final_liquid=None, trades=None, buys=None, sells=None, _id=None):
        self.date_stamp = "" if date_stamp is None else date_stamp
        self.type_info = type_info
        self.ticker = ticker.upper()
        self.period = period
        self.interval = interval
        self.money = money
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
    def static_range(cls, type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id):
        new_entry = cls(type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id)
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trade_money = float(money)
        trade_cost = float(trade_cost)
        buy = float(type_info['buy'])
        sell = float(type_info['sell'])
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
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
                elif available_money>lvalue>0:
                    owned += (lvalue/low)
                    trade_money -= trade_cost
                    trade_money -= lvalue
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
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
                elif owned > available_volume:
                    trade_money += (available_volume*high)
                    trade_money -= trade_cost
                    owned -= available_volume
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
        new_entry.td = td
        new_entry.tt = tt
        new_entry.ty = ty
        new_entry.tp = tp
        new_entry.tv = tv
        new_entry.save_to_mongo()
        return new_entry._id

    @classmethod
    def moving_average(cls, type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id):
        new_entry = cls(type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id)
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trade_money = float(money)
        trade_cost = float(trade_cost)
        bd = float(type_info['buy'])
        sd = float(type_info['sell'])
        trade_cost = float(trade_cost)
        ma_length = int(type_info['length'])
        ma_conv = ma_length - 1
        ma_sum = 0
        td = []  # trade date
        tt = []  # trade time
        ty = []  # trade type
        tp = []  # trade price
        tv = []  # trade volume
        store_ma = []
        store_ma_x = []
        for i in range(0, df.shape[0] - ma_conv):
            for j in range(0, ma_length):
                ma_sum += df.iloc[i + j, 3]
            df.loc[df.index[i + ma_conv], 'SMA_' + str(ma_length)] = np.round((ma_sum / ma_length), 4)
            ma_sum = 0
        for index, row in df.iloc[ma_length:].iterrows():
            count += 1
            available_money = trade_money - trade_cost
            available_volume = row['Volume'] / 40
            low = round(row['Low'], 4)
            high = round(row['High'], 4)
            date = index.to_pydatetime().strftime("%d-%m-%Y")
            time = index.to_pydatetime().strftime("%H:%M")
            lvalue = (low * available_volume)
            hvalue = (high * available_volume)
            buy = row['SMA_' + str(ma_length)] - bd
            sell = row['SMA_' + str(ma_length)] + sd
            store_ma.append(float(row['SMA_' + str(ma_length)]))
            store_ma_x.append(date[6:10] + '-' + date[3:5] + '-' + date[0:2] + 'T' + time + ':00')
            if available_money > 0 and low <= buy and lvalue > trade_cost:
                if lvalue > available_money > 0:
                    owned += (available_money / low)
                    trade_money = 0
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
                elif available_money > lvalue > 0:
                    owned += (lvalue / low)
                    trade_money -= trade_cost
                    trade_money -= lvalue
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
            if owned > 0 and high >= sell and hvalue > trade_cost:
                if available_volume > owned:
                    trade_money += (owned * high)
                    trade_money -= trade_cost
                    owned = 0
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
                elif owned > available_volume:
                    trade_money += (available_volume * high)
                    trade_money -= trade_cost
                    owned -= available_volume
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
        if owned > 0:
            liquid_money = (trade_money - trade_cost) + df.Low.ix[count - 1] * owned
        else:
            liquid_money = trade_money
        new_entry.type_info['ma'] = [store_ma, store_ma_x]
        new_entry.final_money = round(trade_money, 2)
        new_entry.final_owned = round(owned)
        new_entry.final_liquid = round(liquid_money, 2)
        new_entry.td = td
        new_entry.tt = tt
        new_entry.ty = ty
        new_entry.tp = tp
        new_entry.tv = tv
        new_entry.save_to_mongo()
        return new_entry._id

    @classmethod
    def weighted_moving_average(cls, type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id):
        new_entry = cls(type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id)
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        owned = 0
        count = 0
        trade_money = float(money)
        trade_cost = float(trade_cost)
        bd = float(type_info['buy'])
        sd = float(type_info['sell'])
        trade_cost = float(trade_cost)
        wma_length = int(type_info['length'])
        wma_conv = wma_length - 1
        wma_sum = 0
        weight = 0
        weight_sum = 0
        for k in range(1, wma_length + 1):
            weight_sum += k

        td = []  # trade date
        tt = []  # trade time
        ty = []  # trade type
        tp = []  # trade price
        tv = []  # trade volume
        store_wma = []
        store_wma_x = []
        for i in range(0, df.shape[0] - wma_conv):
            for j in range(0, wma_length):
                weight += 1
                wma_sum += (df.iloc[i + j, 3]*weight)
            weight = 0
            df.loc[df.index[i + wma_conv], 'WMA_' + str(wma_length)] = np.round((wma_sum / weight_sum), 4)
            wma_sum = 0
        for index, row in df.iloc[wma_length:].iterrows():
            count += 1
            available_money = trade_money - trade_cost
            available_volume = row['Volume'] / 40
            low = round(row['Low'], 4)
            high = round(row['High'], 4)
            date = index.to_pydatetime().strftime("%d-%m-%Y")
            time = index.to_pydatetime().strftime("%H:%M")
            lvalue = (low * available_volume)
            hvalue = (high * available_volume)
            buy = row['WMA_' + str(wma_length)] - bd
            sell = row['WMA_' + str(wma_length)] + sd
            store_wma.append(float(row['WMA_' + str(wma_length)]))
            store_wma_x.append(date[6:10]+'-'+date[3:5]+'-'+date[0:2]+'T'+time+':00')
            if available_money > 0 and low <= buy and lvalue > trade_cost:
                if lvalue > available_money > 0:
                    owned += (available_money / low)
                    trade_money = 0
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
                elif available_money > lvalue > 0:
                    owned += (lvalue / low)
                    trade_money -= trade_cost
                    trade_money -= lvalue
                    td.append(date)
                    tt.append(time)
                    ty.append('b')
                    tp.append(low)
                    tv.append(available_volume)
            if owned > 0 and high >= sell and hvalue > trade_cost:
                if available_volume > owned:
                    trade_money += (owned * high)
                    trade_money -= trade_cost
                    owned = 0
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
                elif owned > available_volume:
                    trade_money += (available_volume * high)
                    trade_money -= trade_cost
                    owned -= available_volume
                    td.append(date)
                    tt.append(time)
                    ty.append('s')
                    tp.append(high)
                    tv.append(available_volume)
        if owned > 0:
            liquid_money = (trade_money - trade_cost) + df.Low.ix[count - 1] * owned
        else:
            liquid_money = trade_money
        new_entry.type_info['wma'] =  [store_wma, store_wma_x]
        new_entry.final_money = round(trade_money, 2)
        new_entry.final_owned = round(owned)
        new_entry.final_liquid = round(liquid_money, 2)
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
            'type_info': self.type_info,
            'date_stamp': self.date_stamp,
            'ticker': self.ticker,
            'money': self.money,
            'final_money': self.final_money,
            'final_owned': self.final_owned,
            'final_liquid': self.final_liquid,
            'td': self.td,
            'tt': self.tt,
            'ty': self.ty,
            'tp': self.tp,
            'tv': self.tv,
            'period': self.period,
            'interval': self.interval,
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
