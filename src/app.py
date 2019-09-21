from src.common.database import Database
from src.models.calculation import Calculation


from flask import Flask, render_template, request, session

app = Flask(__name__) # '__main__'
app.secret_key = "Michael"

@app.route('/')
def home_template():
    return render_template('home.html')

@app.route('/login')
def login_template():
    return render_template('login.html')

@app.before_first_request
def initialize_database():
    Database.initialize()

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
    return_message = []

    valid = [Submission.verify_ticker(ticker),
            Submission.verify_money(money)]
    if valid == [True, True]:
        final_money = Calculation.algo(ticker, period, interval, money, buy, sell)
    else:
        for entry in valid:
            error_message = ["The ticker you entered was not valid",
                              "The money you entered was not valid"]
            if valid[entry] == False:
                return_message += error_message[entry]
            elif valid[entry] == True:
                return_message += Null
    transaction_id = Calculation.algo(ticker, period, interval, money, buy, sell)
    url = "/results/" + str(transaction_id)
    return render_template(url)

@app.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results=Calculation.from_mongo(transaction_id)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(port=4996)