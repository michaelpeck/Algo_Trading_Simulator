__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, session, Blueprint
from src.users.user import User
from src.posts.post import Post

posts = Blueprint('posts', __name__)

@posts.route('/forum')
def get_posts():
    posts = Post.all_posts()

    return render_template('/forum.html', posts=posts)

@posts.route('/new_post')
def new_post_template():
    return render_template('new_post.html')

@posts.route('/post/new', methods=['POST'])
def create_post():
    title = request.form['title']
    content = request.form['content']

    user = User.get_id_by_email(session['email'])
    user_id = user.user_id
    author = user.first_name
    Post.create_post(user_id, title, content, author)

    return render_template('/forum.html')
