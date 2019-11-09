__author__ = 'michaelpeck'

from flask import Flask, render_template, request, redirect, url_for, Blueprint, flash
from flask_login import current_user, login_required
from src.users.user import User
from src.posts.post import Post
import datetime as dt
from src.posts.forms import (NewPostForm)

posts = Blueprint('posts', __name__)

@posts.route('/forum')
def forum():
    posts = Post.objects()
    return render_template('/forum.html', posts=posts)

@posts.route("/new_post", methods=['Get', 'POST'])
@login_required
def new_post():
    form = NewPostForm()
    if form.validate_on_submit():
        Post(title=form.title.data, date=dt.datetime.utcnow(), content=form.content.data,
             author=current_user.username, owner=current_user.id).save()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.forum'))
    return render_template('new_post.html', title='New Post', form=form)
