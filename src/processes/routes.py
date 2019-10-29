__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint
from src.users.user import User
from src.processes.models import Model
from src.processes.calculation import Calculation
from src.posts.post import Post
import datetime as dt


processes = Blueprint('processes', __name__)

@processes.route('/static_range')
def static_range_template():
    mod = ""
    return render_template('static_range.html', mod=mod)

@processes.route('/static_range/<string:model_id>')
def static_range_template_model(model_id):
    mod = Model.get_by_id(model_id)
    return render_template('static_range.html', mod=mod)

@processes.route('/moving_average')
def moving_average_template():
    return render_template('moving_average.html')

@processes.route('/weighted_moving_average')
def weighted_moving_average_template():
    return render_template('weighted_moving_average.html')

@processes.route('/calc/static_range', methods=['POST'])
def calc_static_range():
    ticker = request.form['ticker']
    period = request.form['period']
    interval = request.form['interval']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    date_stamp = dt.datetime.now()
    type_info = {'type': 'SR',
                 'buy': buy,
                 'sell': sell}
    if session['email'] != None:
        user = User.get_id_by_email(session['email'])
        user_id = user.user_id
    else:
        user_id = "guest"

    model_id = Model.create_model(ticker, period, interval, money, buy, sell, trade_cost, user_id)
    transaction = Calculation.static_range(type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id)
    url = "/results/" + transaction
    return redirect(url)

@processes.route('/calc/moving_average', methods=['POST'])
def calc_moving_average():
    ticker = request.form['ticker']
    period = request.form['period']
    interval = '1d'
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    date_stamp = dt.datetime.now()
    type_info = {'type': 'MA',
                 'buy': buy,
                 'sell': sell}
    if session['email'] != None:
        user = User.get_id_by_email(session['email'])
        user_id = user.user_id
    else:
        user_id = "guest"

    model_id = Model.create_model(ticker, period, interval, money, buy, sell, trade_cost, user_id)
    transaction = Calculation.moving_average(type_info, ticker, period, interval, money, trade_cost, user_id, date_stamp, model_id)
    url = "/results/" + transaction
    return redirect(url)

@processes.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results = Calculation.from_mongo(transaction_id)
    return render_template('results.html', results=results)

@processes.route('/entry/<string:transaction_id>')
def get_entry(transaction_id):
    entry = Calculation.from_mongo(transaction_id)
    return render_template('entry.html', entry=entry)

@processes.route('/delete/<string:transaction_id>')
def delete_entry(transaction_id):
    Calculation.delete_entry_by_id(transaction_id)
    user = User.get_by_email(session['email'])
    entries = user.get_entries()
    models = user.get_models()
    user_id = user.get_id()
    posts = Post.from_user(user_id)

    return render_template("profile.html", user=user, entries=entries, models=models, posts=posts, email=session['email'])
