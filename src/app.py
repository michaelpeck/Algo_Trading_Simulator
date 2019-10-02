from src.common.database import Database
from src.models.calculation import Calculation
from src.models.user import User
from src.models.processing import Submission


from flask import Flask, render_template, request, redirect, session

app = Flask(__name__) # '__main__'
app.secret_key = "Michael"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/about')
def about_template():
    return render_template('about.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.route('/register')
def register_template():
    return render_template('register.html')

@app.route('/logout')
def log_out():
    User.logout()
    return render_template("home.html")

@app.before_first_request
def initialize_database():
    Database.initialize()
    session['email'] = None

@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email, password):
        User.login(email)
        user = User.get_by_email(session['email'])
        entries = user.get_entries()
        return render_template("profile.html", user=user, entries=entries, email=session['email'])
    else:
        session['email'] = None
        return render_template("login.html")


@app.route('/auth/register', methods=['POST'])
def register_user():
    first_name = request.form['first']
    last_name = request.form['last']
    email = request.form['email']
    password = request.form['password']
    User.register(first_name, last_name, email, password)

    return render_template("profile.html", email=session['email'])

@app.route('/profile')
def profile_template():
    user = User.get_by_email(session['email'])
    entries = user.get_entries()

    return render_template("profile.html", user=user, entries=entries, email=session['email'])

@app.route('/strategies')
def strategies_template():
    return render_template('strategies.html')

@app.route('/static_range')
def static_range_template():
    return render_template('static_range.html')

@app.route('/moving_average')
def moving_average_template():
    return render_template('moving_average.html')

@app.route('/weighted_moving_average')
def weighted_moving_average_template():
    return render_template('weighted_moving_average.html')

@app.route('/calc/static_range', methods=['POST'])
def calc_data():
    ticker = request.form['ticker']
    period = request.form['period']
    interval = request.form['interval']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    trade_cost = request.form['trade_cost']
    if session['email'] != None:
        user = User.get_id_by_email(session['email'])
        user_id = user.user_id
    else:
        user_id = "guest"

    transaction = Calculation.static_range("SR", ticker, period, interval, money, buy, sell, trade_cost, user_id)
    url = "/results/" + transaction

    return redirect(url)

@app.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results = Calculation.from_mongo(transaction_id)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(port=4996)