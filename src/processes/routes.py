__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint
from src.users.user import User
from src.processes.models import Model
from src.processes.calculation import Calculation


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
def calc_data():
    ticker = request.form['ticker']
    period = request.form['period']
    interval = request.form['interval']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    model_name = request.form['model_name']

    if session['email'] != None:
        user = User.get_id_by_email(session['email'])
        user_id = user.user_id
    else:
        user_id = "guest"

    model_id = Model.create_model(ticker, period, interval, money, buy, sell, trade_cost, model_name, user_id)
    transaction = Calculation.static_range("SR", ticker, period, interval, money, buy, sell, trade_cost, user_id, model_id)
    url = "/results/" + transaction
    return redirect(url)

@processes.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results = Calculation.from_mongo(transaction_id)

    return render_template('results.html', results=results)