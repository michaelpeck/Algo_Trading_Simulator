from src.common.database import Database
from src.models.calculation import Calculation
from src.models.user import User
from src.models.processing import Submission
from src.models.strategy_model import Model
from src.models.post import Post


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
        models = user.get_models()
        user_id = user.get_id()
        posts = Post.from_user(user_id)
        return render_template("profile.html", user=user, entries=entries, models=models, posts=posts, email=session['email'])
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
    models = user.get_models()
    user_id = user.get_id()
    posts = Post.from_user(user_id)

    return render_template("profile.html", user=user, entries=entries, models=models , posts=posts, email=session['email'])

@app.route('/strategies')
def strategies_template():
    return render_template('strategies.html')

@app.route('/static_range')
def static_range_template():
    model = Model.get_by_id('5c5c5651b3144092ab2b8bf5f4daeada')
    return render_template('static_range.html', model=model)

@app.route('/static_range/<string:model_id>')
def static_range_template_model(model_id):
    model = Model.get_by_id(model_id)
    return render_template('static_range.html', model=model)

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


@app.route('/results/<string:transaction_id>')
def get_results(transaction_id):
    results = Calculation.from_mongo(transaction_id)

    return render_template('results.html', results=results)

@app.route('/forum')
def get_posts():
    posts = Post.all_posts()

    return render_template('/forum.html', posts=posts)

@app.route('/new_post')
def new_post_template():
    return render_template('new_post.html')

@app.route('/post/new', methods=['POST'])
def create_post():
    title = request.form['title']
    content = request.form['content']

    user = User.get_id_by_email(session['email'])
    user_id = user.user_id
    author = user.first_name
    Post.create_post(user_id, title, content, author)

    return render_template('/forum.html')




if __name__ == '__main__':
    app.run(port=4996)