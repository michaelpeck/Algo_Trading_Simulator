__author__ = 'michaelpeck'

from src import db
from flask_login import UserMixin


class Post(UserMixin, db.Document):
    meta = {'collection': 'posts'}
    title = db.StringField(max_length=30)
    date = db.DateTimeField()
    content = db.StringField(max_length=1000)
    author = db.StringField(max_length=30)
    tags = db.ListField()
    owner = db.LazyReferenceField('User')