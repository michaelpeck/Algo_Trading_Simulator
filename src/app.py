from src.common.database import Database


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

@app.route('/stock_data.html')
def data_entry_template():
    return render_template('stock_data.html')

@app.route('/calc/stock_data', methods=['POST'])
def calc_data():
    ticker = request.form['ticker']
    start = request.form['start']
    end = request.form['end']
    money = request.form['money']
    trade_point = request.form['trade_point']
    return_message = []

    valid = [Submission.verify_ticker(ticker),
            Submission.verify_date(start),
            Submission.verify_date(end),
            Submission.verify_money(money)]
    if valid == [True, True, True, True]:
        final_money = Calculation.algo(ticker, start, end, money, trade_point)
    else:
        for entry in valid:
            error_message = ["The ticker you entered was not valid",
                             "The start date you entered was not valid",
                             "The end date you entered was not valid",
                              "The money you entered was not valid"]
            if valid[entry] == False:
                return_message += error_message[entry]
            elif valid[entry] == True:
                return_message += Null

    return Calculation.algo(ticker, start, end, money, trade_point)

if __name__ == '__main__':
    app.run(port=4996)