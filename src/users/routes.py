__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint
from src.users.user import User
from src.posts.post import Post


users = Blueprint('users', __name__)

@users.route('/login')
def login_template():
    return render_template('login.html')

@users.route('/register')
def register_template():
    return render_template('register.html')

@users.route('/logout')
def log_out():
    User.logout()
    return render_template("home.html")

@users.route('/auth/login', methods=['POST'])
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


@users.route('/auth/register', methods=['POST'])
def register_user():
    first_name = request.form['first']
    last_name = request.form['last']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    User.register(first_name, last_name, username, email, password)
    User.login(email)
    user = User.get_by_email(session['email'])
    entries = user.get_entries()
    models = user.get_models()
    user_id = user.get_id()
    posts = Post.from_user(user_id)
    return render_template("profile.html", user=user, entries=entries, models=models, posts=posts,
                           email=session['email'])

@users.route('/profile')
def profile_template():
    user = User.get_by_email(session['email'])
    entries = user.get_entries()
    models = user.get_models()
    user_id = user.get_id()
    posts = Post.from_user(user_id)

    return render_template("profile.html", user=user, entries=entries, models=models , posts=posts, email=session['email'])
