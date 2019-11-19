__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint, flash, url_for
from flask_login import current_user
from src.processes.models import Model, UserModel
from src.processes.calculation import Calculation
from src.processes.check import Check
from src.posts.post import Post
from src.processes.forms import (StaticRangeForm, MovingAverageForm, WeightedMovingAverageForm, TryAgain, SaveEntry,
                                 SaveModel, PickModel, StockDataForm)
import datetime as dt


processes = Blueprint('processes', __name__)

@processes.route('/range', methods=['GET', 'POST'])
@processes.route('/range/<string:model_id>', methods=['GET', 'POST'])
def static_range_template(model_id=None):
    form = StaticRangeForm()
    mform = PickModel()
    sform = StockDataForm()
    choices = [('', 'No model')]
    stock_info = ''
    if current_user.is_authenticated:
        models = current_user.get_models()
        if models:
            for model in models:
                if model.mod_type == "SR":
                    choices.append((model.id, model.name))
    mform.model.choices = choices
    if mform.pop_model.data and (mform.model.data != ''):
        return redirect(url_for('processes.static_range_template', model_id=mform.model.data))
    if sform.check.data:
        info = Check(ticker=sform.check_ticker.data.upper()).get_info()
        stock_info = Check.objects(pk=info).first()
    if form.submit.data and form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='SR',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         interval=form.interval.data,
                         money=form.money.data,
                         buy=form.buy.data,
                         sell=form.sell.data,
                         trade_cost=form.trade_cost.data).save()
        sr_calc = Calculation(type_info='SR',
                              ticker=form.ticker.data,
                              period=form.period.data,
                              interval=form.interval.data,
                              buy=form.buy.data,
                              sell=form.sell.data,
                              money=form.money.data,
                              trade_cost=form.trade_cost.data,
                              date_stamp=date_stamp,
                              model=this_mod.id).static_range()
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_r_results', transaction_id=sr_calc))
    elif request.method == 'GET':
        if model_id:
            if Model.objects(pk=model_id):
                mod = Model.objects(pk=model_id).first()
                form.ticker.data = mod.ticker
            else:
                mod = UserModel.objects(pk=model_id).first()
                mform.model.data = model_id
            form.period.data = mod.period
            form.interval.data = mod.interval
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
    return render_template('static_range.html', title='Static Range', form=form, mform=mform, sform=sform, stock_info=stock_info)

@processes.route('/moving_average', methods=['GET', 'POST'])
@processes.route('/moving_average/<string:model_id>', methods=['GET', 'POST'])
def moving_average_template(model_id=None):
    form = MovingAverageForm()
    mform = PickModel()
    sform = StockDataForm()
    choices = [('', 'No model')]
    stock_info = ''
    if current_user.is_authenticated:
        models = current_user.get_models()
        if models:
            for model in models:
                if model.mod_type == 'MA':
                    choices.append((model.id, model.name))
    mform.model.choices = choices
    if mform.pop_model.data and (mform.model.data != ''):
        return redirect(url_for('processes.static_range_template', model_id=mform.model.data))
    if sform.check.data:
        info = Check(ticker=sform.check_ticker.data.upper()).get_info()
        stock_info = Check.objects(pk=info).first()
    if form.submit.data and form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='MA',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         av_length=form.length.data,
                         money=form.money.data,
                         buy=form.buy.data,
                         sell=form.sell.data,
                         trade_cost=form.trade_cost.data).save()
        ma_calc = Calculation(type_info='MA',
                              ticker=form.ticker.data,
                              period=form.period.data,
                              av_length=form.length.data,
                              buy=form.buy.data,
                              sell=form.sell.data,
                              money=form.money.data,
                              trade_cost=form.trade_cost.data,
                              date_stamp=date_stamp,
                              model=this_mod.id).moving_average()
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_ma_results', transaction_id=ma_calc))
    elif request.method == 'GET':
        if model_id:
            if Model.objects(pk=model_id):
                mod = Model.objects(pk=model_id).first()
                form.ticker.data = mod.ticker
            else:
                mod = UserModel.objects(pk=model_id).first()
                mform.model.data = model_id
            form.ticker.data = mod.ticker
            form.period.data = mod.period
            form.length.data = mod.av_length
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
    return render_template('moving_average.html', title='Moving Average', form=form, mform=mform, sform=sform, stock_info=stock_info)

@processes.route('/weighted_moving_average', methods=['GET', 'POST'])
@processes.route('/weighted_moving_average/<string:model_id>', methods=['GET', 'POST'])
def weighted_moving_average_template(model_id=None):
    form = WeightedMovingAverageForm()
    mform = PickModel()
    sform = StockDataForm()
    choices = [('', 'No model')]
    stock_info = ''
    if current_user.is_authenticated:
        models = current_user.get_models()
        if models:
            for model in models:
                if model.mod_type == 'WMA':
                    choices.append((model.id, model.name))
    mform.model.choices = choices
    if mform.pop_model.data and (mform.model.data != ''):
        return redirect(url_for('processes.static_range_template', model_id=mform.model.data))
    if sform.check.data:
        info = Check(ticker=sform.check_ticker.data.upper()).get_info()
        stock_info = Check.objects(pk=info).first()
    if form.submit.data and form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='WMA',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         av_length=form.length.data,
                         money=form.money.data,
                         buy=form.buy.data,
                         sell=form.sell.data,
                         trade_cost=form.trade_cost.data).save()
        wma_calc = Calculation(type_info='WMA',
                               ticker=form.ticker.data,
                               period=form.period.data,
                               av_length=form.length.data,
                               buy=form.buy.data,
                               sell=form.sell.data,
                               money=form.money.data,
                               trade_cost=form.trade_cost.data,
                               date_stamp=date_stamp,
                               model=this_mod.id).moving_average()
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_wma_results', transaction_id=wma_calc))
    elif request.method == 'GET':
        if model_id:
            if Model.objects(pk=model_id):
                mod = Model.objects(pk=model_id).first()
                form.ticker.data = mod.ticker
            else:
                mod = UserModel.objects(pk=model_id).first()
                mform.model.data = model_id
            form.ticker.data = mod.ticker
            form.period.data = mod.period
            form.length.data = mod.av_length
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
    return render_template('weighted_moving_average.html', title='Weighted Moving Average', form=form, mform=mform, sform=sform, stock_info=stock_info)

@processes.route('/r_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_r_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if not results.owner:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.static_range_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(owner=current_user.id)
    if mform.validate_on_submit() and mform.savemodel.data:
        mod = Model.objects(pk=results.model.id).first()
        if not Calculation.objects(pk=transaction_id).first().user_model:
            name = 'SR-'+ str(len(UserModel.objects(owner=current_user.id))+1)
            saved_mod = UserModel(name=name,
                                  mod_type=mod.mod_type,
                                  period=mod.period,
                                  interval=mod.interval,
                                  money=mod.money,
                                  buy=mod.buy,
                                  sell=mod.sell,
                                  trade_cost=mod.trade_cost,
                                  owner=current_user.id).save()
            Calculation.objects(pk=transaction_id).update_one(user_model=saved_mod.id)
    return render_template('r_results.html', results=results, form=form, eform=eform, mform=mform)

@processes.route('/ma_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_ma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if not results.owner:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.moving_average_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(owner=current_user.id)
    if mform.validate_on_submit() and mform.savemodel.data:
        mod = Model.objects(pk=results.model.id).first()
        if not Calculation.objects(pk=transaction_id).first().user_model:
            name = 'MA-' + str(len(UserModel.objects(owner=current_user.id)) + 1)
            saved_mod = UserModel(name=name,
                                  mod_type=mod.mod_type,
                                  period=mod.period,
                                  av_length=mod.av_length,
                                  money=mod.money,
                                  buy=mod.buy,
                                  sell=mod.sell,
                                  trade_cost=mod.trade_cost,
                                  owner=current_user.id).save()
            Calculation.objects(pk=transaction_id).update_one(user_model=saved_mod.id)
    return render_template('ma_results.html', results=results, form=form, eform=eform, mform=mform)

@processes.route('/wma_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_wma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if not results.owner:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.weighted_moving_average_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(owner=current_user.id)
    if mform.validate_on_submit() and mform.savemodel.data:
        mod = Model.objects(pk=results.model.id).first()
        if not Calculation.objects(pk=transaction_id).first().user_model:
            name = 'WMA-' + str(len(UserModel.objects(owner=current_user.id)) + 1)
            saved_mod = UserModel(name=name,
                                  mod_type=mod.mod_type,
                                  period=mod.period,
                                  av_length=mod.av_length,
                                  money=mod.money,
                                  buy=mod.buy,
                                  sell=mod.sell,
                                  trade_cost=mod.trade_cost,
                                  owner=current_user.id).save()
            Calculation.objects(pk=transaction_id).update_one(user_model=saved_mod.id)
    return render_template('wma_results.html', results=results, form=form, eform=eform, mform=mform)

@processes.route('/sr_entry/<string:transaction_id>')
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
    if Calculation.objects(pk=transaction_id).first():
        Calculation.objects(pk=transaction_id).first().delete()
    user = current_user
    entries = user.get_entries()
    models = user.get_models()
    posts = Post.objects(owner=user.id)
    image_file = url_for('static', filename='assets/profile_pics/' + current_user.image_file)
    return render_template("profile.html", user=user, entries=entries, models=models, posts=posts, image_file=image_file)
