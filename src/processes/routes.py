__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint, flash, url_for
from flask_login import current_user
from src.processes.models import Model
from src.processes.calculation import Calculation
from src.posts.post import Post
from src.processes.forms import (StaticRangeForm)
import datetime as dt


processes = Blueprint('processes', __name__)

@processes.route('/range', methods=['GET', 'POST'])
def static_range_template():
    mod = ""
    date_stamp = str(dt.datetime.now())
    form = StaticRangeForm()
    if form.validate_on_submit():
        sr_calc = Calculation(type_info='SR', ticker=form.ticker.data, period=form.period.data, interval=form.interval.data,
                              buy=form.buy.data, sell=form.sell.data, money=form.money.data, trade_cost=form.trade_cost.data,
                              date_stamp=date_stamp).static_range()
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('get_r_results', transaction_id=sr_calc.id))
    return render_template('static_range.html', title='Static Range', mod=mod, form=form)

@processes.route('/range/<string:model_id>')
def static_range_template_model(model_id):
    mod = Model.objects(pk=model_id).first()
    return render_template('static_range.html', mod=mod)

@processes.route('/moving_average')
def moving_average_template():
    mod = ""
    return render_template('moving_average.html', mod=mod)

@processes.route('/moving_average/<string:model_id>')
def moving_average_template_model(model_id):
    mod = Model.objects(pk=model_id).first()
    return render_template('moving_average.html', mod=mod)

@processes.route('/weighted_moving_average')
def weighted_moving_average_template():
    mod = ""
    return render_template('weighted_moving_average.html', mod=mod)

@processes.route('/weighted_moving_average/<string:model_id>')
def weighted_moving_average_template_model(model_id):
    mod = Model.objects(pk=model_id).first()
    return render_template('weighted_moving_average.html', mod=mod)

@processes.route('/calc/static_range', methods=['POST'])
def calc_static_range():
    ticker = request.form['ticker'].upper()
    period = request.form['period']
    interval = request.form['interval']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    date_stamp = str(dt.datetime.now())
    type_info = 'SR'
    if current_user.is_authenticated:
        user_id = current_user.id
        this_mod = Model(mod_type='SR', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost, owner=user_id).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, owner=user_id, date_stamp=date_stamp,
                                  model=this_mod.id).static_range()
    else:
        this_mod = Model(mod_type='SR', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, date_stamp=date_stamp,
                                  model=this_mod.id).static_range()

    url = "/r_results/" + str(transaction)
    return redirect(url)

@processes.route('/calc/moving_average', methods=['POST'])
def calc_moving_average():
    ticker = request.form['ticker'].upper()
    period = request.form['period']
    interval = '1d'
    length = request.form['length']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    date_stamp = str(dt.datetime.now())
    type_info = 'MA'
    if current_user.is_authenticated:
        user_id = current_user.id
        this_mod = Model(mod_type='MA', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost, av_length=length, owner=user_id).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, owner=user_id, date_stamp=date_stamp,
                                  model=this_mod.id, av_length=length).moving_average()
    else:
        this_mod = Model(mod_type='MA', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost, av_length=length).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, date_stamp=date_stamp,
                                  model=this_mod.id, av_length=length).moving_average()

    url = "/ma_results/" + str(transaction)
    return redirect(url)

@processes.route('/calc/weighted_moving_average', methods=['POST'])
def calc_weighted_moving_average():
    ticker = request.form['ticker'].upper()
    period = request.form['period']
    interval = '1d'
    length = request.form['length']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    date_stamp = str(dt.datetime.now())
    type_info = 'WMA'
    if current_user.is_authenticated:
        user_id = current_user.id
        this_mod = Model(mod_type='WMA', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost, av_length=length, owner=user_id).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, owner=user_id, date_stamp=date_stamp,
                                  model=this_mod.id, av_length=length).weighted_moving_average()
    else:
        this_mod = Model(mod_type='WMA', ticker=ticker, period=period, interval=interval, money=money, buy=buy,
                         sell=sell, trade_cost=trade_cost, av_length=length).save()
        transaction = Calculation(type_info=type_info, ticker=ticker, period=period, interval=interval, buy=buy,
                                  sell=sell, money=money, trade_cost=trade_cost, date_stamp=date_stamp,
                                  model=this_mod.id, av_length=length).weighted_moving_average()

    url = "/wma_results/" + str(transaction)
    return redirect(url)

@processes.route('/r_results/<string:transaction_id>')
def get_r_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    return render_template('r_results.html', results=results)

@processes.route('/ma_results/<string:transaction_id>')
def get_ma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    return render_template('ma_results.html', results=results)

@processes.route('/wma_results/<string:transaction_id>')
def get_wma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    return render_template('wma_results.html', results=results)

@processes.route('/r_entry/<string:transaction_id>')
def get_r_entry(transaction_id):
    entry = Calculation.objects(pk=transaction_id).first()
    return render_template('r_entry.html', entry=entry)

@processes.route('/ma_entry/<string:transaction_id>')
def get_ma_entry(transaction_id):
    entry = Calculation.objects(pk=transaction_id).first()
    return render_template('ma_entry.html', entry=entry)

@processes.route('/wma_entry/<string:transaction_id>')
def get_wma_entry(transaction_id):
    entry = Calculation.objects(pk=transaction_id).first()
    return render_template('wma_entry.html', entry=entry)

@processes.route('/delete/<string:transaction_id>')
def delete_entry(transaction_id):
    Calculation.objects(pk=transaction_id).first().delete()
    user = current_user
    entries = user.get_entries()
    models = user.get_models()
    user_id = user.id
    posts = Post.from_user(user_id)

    return render_template("profile.html", user=user, entries=entries, models=models, posts=posts, email=session['email'])
