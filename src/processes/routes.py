__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint, flash, url_for
from flask_login import current_user
from src.processes.models import Model
from src.processes.calculation import Calculation
from src.posts.post import Post
from src.processes.forms import (StaticRangeForm, MovingAverageForm, WeightedMovingAverageForm, TryAgain, SaveEntry, SaveModel)
import datetime as dt


processes = Blueprint('processes', __name__)

@processes.route('/range', methods=['GET', 'POST'])
@processes.route('/range/<string:model_id>', methods=['GET', 'POST'])
def static_range_template(model_id=None):
    form = StaticRangeForm()
    if form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='SR',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         interval=form.interval.data,
                         money=form.money.data,
                         buy=form.buy.data,
                         sell=form.sell.data,
                         trade_cost=form.trade_cost.data,
                         keep=False).save()
        sr_calc = Calculation(type_info='SR',
                              ticker=form.ticker.data,
                              period=form.period.data,
                              interval=form.interval.data,
                              buy=form.buy.data,
                              sell=form.sell.data,
                              money=form.money.data,
                              trade_cost=form.trade_cost.data,
                              date_stamp=date_stamp,
                              model=this_mod.id,
                              keep=False).static_range()
        if current_user.is_authenticated:
            user_id = current_user.id
            Model.objects(pk=this_mod.id).update_one(owner=user_id)
            Calculation.objects(pk=sr_calc).update_one(owner=user_id)
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_r_results', transaction_id=sr_calc))
    elif request.method == 'GET':
        if model_id:
            mod = Model.objects(pk=model_id).first()
            form.ticker.data = mod.ticker
            form.period.data = mod.period
            form.interval.data = mod.interval
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
            if mod.keep is False:
                Model.objects(pk=model_id).delete()
    return render_template('static_range.html', title='Static Range', form=form)

@processes.route('/moving_average', methods=['GET', 'POST'])
@processes.route('/moving_average/<string:model_id>', methods=['GET', 'POST'])
def moving_average_template(model_id=None):
    form = MovingAverageForm()
    if form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='MA',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         av_length=form.length.data,
                         money=form.money.data,
                         buy=form.buy.data, sell=form.sell.data,
                         trade_cost=form.trade_cost.data,
                         keep=False).save()
        ma_calc = Calculation(type_info='MA',
                              ticker=form.ticker.data,
                              period=form.period.data,
                              av_length=form.length.data,
                              buy=form.buy.data,
                              sell=form.sell.data,
                              money=form.money.data,
                              trade_cost=form.trade_cost.data,
                              date_stamp=date_stamp,
                              model=this_mod.id,
                              keep=False).moving_average()
        if current_user.is_authenticated:
            user_id = current_user.id
            Model.objects(pk=this_mod.id).update_one(owner=user_id)
            Calculation.objects(pk=ma_calc).update_one(owner=user_id)
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_ma_results', transaction_id=ma_calc))
    elif request.method == 'GET':
        if model_id:
            mod = Model.objects(pk=model_id).first()
            form.ticker.data = mod.ticker
            form.period.data = mod.period
            form.length.data = mod.av_length
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
            if mod.keep is False:
                Model.objects(pk=model_id).delete()
    return render_template('moving_average.html', title='Moving Average', form=form)

@processes.route('/weighted_moving_average', methods=['GET', 'POST'])
@processes.route('/weighted_moving_average/<string:model_id>', methods=['GET', 'POST'])
def weighted_moving_average_template(model_id=None):
    form = WeightedMovingAverageForm()
    if form.validate_on_submit():
        date_stamp = str(dt.datetime.now())
        this_mod = Model(mod_type='WMA',
                         ticker=form.ticker.data,
                         period=form.period.data,
                         av_length=form.length.data,
                         money=form.money.data,
                         buy=form.buy.data,
                         sell=form.sell.data,
                         trade_cost=form.trade_cost.data,
                         keep=False).save()
        wma_calc = Calculation(type_info='WMA',
                               ticker=form.ticker.data,
                               period=form.period.data,
                               av_length=form.length.data,
                               buy=form.buy.data,
                               sell=form.sell.data,
                               money=form.money.data,
                               trade_cost=form.trade_cost.data,
                               date_stamp=date_stamp,
                               model=this_mod.id,
                               keep=False).moving_average()
        if current_user.is_authenticated:
            user_id = current_user.id
            Model.objects(pk=this_mod.id).update_one(owner=user_id)
            Calculation.objects(pk=wma_calc).update_one(owner=user_id)
        flash('Your calculation is complete!', 'success')
        return redirect(url_for('processes.get_wma_results', transaction_id=wma_calc))
    elif request.method == 'GET':
        if model_id:
            mod = Model.objects(pk=model_id).first()
            form.ticker.data = mod.ticker
            form.period.data = mod.period
            form.length.data = mod.av_length
            form.money.data = mod.money
            form.buy.data = mod.buy
            form.sell.data = mod.sell
            form.trade_cost.data = mod.trade_cost
            if mod.keep is False:
                Model.objects(pk=model_id).delete()
    return render_template('weighted_moving_average.html', title='Weighted Moving Average', form=form)

@processes.route('/r_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_r_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if results.keep is False:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.static_range_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(keep=True)
    if mform.validate_on_submit() and mform.savemodel.data:
        Model.objects(pk=results.model.id).update_one(keep=True)
    return render_template('r_results.html', results=results, form=form, eform=eform, mform=mform)

@processes.route('/ma_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_ma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if results.keep is False:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.moving_average_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(keep=True)
    if mform.validate_on_submit() and mform.savemodel.data:
        Model.objects(pk=results.model.id).update_one(keep=True)
    return render_template('ma_results.html', results=results, form=form, eform=eform, mform=mform)

@processes.route('/wma_results/<string:transaction_id>', methods=['GET', 'POST'])
def get_wma_results(transaction_id):
    results = Calculation.objects(pk=transaction_id).first()
    form = TryAgain()
    eform = SaveEntry()
    mform = SaveModel()
    if form.validate_on_submit() and form.submit.data:
        if results.keep is False:
            Calculation.objects(pk=transaction_id).delete()
        return redirect(url_for('processes.weighted_moving_average_template', model_id=str(results.model.id)))
    if eform.validate_on_submit() and eform.saveentry.data:
        Calculation.objects(pk=transaction_id).update_one(keep=True)
    if mform.validate_on_submit() and mform.savemodel.data:
        Model.objects(pk=results.model.id).update_one(keep=True)
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
    Calculation.objects(pk=transaction_id).first().delete()
    user = current_user
    entries = user.get_entries()
    models = user.get_models()
    user_id = user.id
    posts = Post.from_user(user_id)

    return render_template("profile.html", user=user, entries=entries, models=models, posts=posts, email=session['email'])
