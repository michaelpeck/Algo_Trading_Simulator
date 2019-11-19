import yfinance as yf
import numpy as np
import datetime
from src.common.database import Database
from flask_login import current_user, UserMixin
from src import db


class Calculation(UserMixin, db.Document):
    meta = {'collection': 'entries'}
    keep = db.BooleanField(default=True)
    date_stamp = db.StringField(max_length=40)
    type_info = db.StringField()
    buy = db.FloatField()
    sell = db.FloatField()
    av_length = db.IntField()
    ticker = db.StringField()
    period = db.StringField()
    interval = db.StringField()
    money = db.FloatField()
    trade_cost = db.FloatField()
    owner = db.LazyReferenceField('User')
    final_money = db.FloatField()
    final_owned = db.FloatField()
    final_liquid = db.FloatField()
    td = db.ListField()
    tt = db.ListField()
    ty = db.ListField()
    tp = db.ListField()
    tv = db.ListField()
    graph_x = db.ListField()
    graph_y = db.ListField()
    model = db.LazyReferenceField('Model')
    user_model = db.LazyReferenceField('UserModel')


    def static_range(self):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period=self.period, interval=self.interval)
        owned = 0
        count = 0
        trade_money = self.money
        trade_cost = self.trade_cost
        buy = self.buy
        sell = self.sell
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
        self.final_money = round(trade_money, 2)
        self.final_owned = round(owned)
        self.final_liquid = round(liquid_money, 2)
        self.td = td
        self.tt = tt
        self.ty = ty
        self.tp = tp
        self.tv = tv
        self.save()
        return self.id

    def moving_average(self):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period=self.period, interval='1d')
        owned = 0
        count = 0
        trade_money = self.money
        trade_cost = self.trade_cost
        bd = self.buy
        sd = self.sell
        ma_length = self.av_length
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
        self.graph_y = store_ma
        self.graph_x = store_ma_x
        self.final_money = round(trade_money, 2)
        self.final_owned = round(owned)
        self.final_liquid = round(liquid_money, 2)
        self.td = td
        self.tt = tt
        self.ty = ty
        self.tp = tp
        self.tv = tv
        self.save()
        return self.id

    def weighted_moving_average(self):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period=self.period, interval='1d')
        owned = 0
        count = 0
        trade_money = self.money
        trade_cost = self.trade_cost
        bd = self.buy
        sd = self.sell
        wma_length = self.av_length
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
        self.graph_x = store_wma_x
        self.graph_y = store_wma
        self.final_money = round(trade_money, 2)
        self.final_owned = round(owned)
        self.final_liquid = round(liquid_money, 2)
        self.td = td
        self.tt = tt
        self.ty = ty
        self.tp = tp
        self.tv = tv
        self.save()
        return self.id

