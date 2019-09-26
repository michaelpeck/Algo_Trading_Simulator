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
        return render_template("profile.html", email=session['email'])
    else:
        session['email'] = None
        return render_template("login.html")


@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']
    User.register(email, password)

    return render_template("profile.html", email=session['email'])

@app.route('/profile')
def profile_template():
    return render_template("profile.html", email=session['email'])


@app.route('/stock_data')
def data_entry_template():
    return render_template('stock_data.html')

@app.route('/calc/stock_data', methods=['POST'])
def calc_data():
    ticker = request.form['ticker']
    period = request.form['period']
    interval = request.form['interval']
    money = request.form['money']
    buy = request.form['buy']
    sell = request.form['sell']
    if session['email'] != None:
        user_id = User.get_id_by_email(session['email'])
    else:
        user_id = "guest"

    transaction = Calculation.algo(ticker, period, interval, money, buy, sell, user_id)
    url = "/results/" + transaction

    return redirect(url)

@app.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results = Calculation.from_mongo(transaction_id)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(port=4996)