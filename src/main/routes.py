from flask import Flask, render_template, request, redirect, session, Blueprint
from src.common.database import Database

main = Blueprint('main', __name__)

@main.route("/")
def home_template():
    return render_template('home.html')

@main.route('/about')
def about_template():
    return render_template('about.html')

@main.route('/strategies')
def strategies_template():
    return render_template('strategies.html')
