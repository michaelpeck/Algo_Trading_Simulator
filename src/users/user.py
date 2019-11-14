
from datetime import datetime
from src.processes.calculation import Calculation
from src.processes.models import Model
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
from flask_mongoengine import MongoEngine, Document
from src import db, login_manager


__author__ = 'michaelpeck'

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()


class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    username = db.StringField(max_length=20)
    email = db.StringField(max_length=30)
    password = db.StringField()
    image_file = db.StringField(default='default.jpg')
    bio = db.StringField(max_length=200, default='This is my bio...')
    entries = db.LazyReferenceField('Calculation')
    models = db.LazyReferenceField('Model')
    posts = db.LazyReferenceField('Post')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


    def get_entries(self):
        return Calculation.objects(owner=self.id)

    def get_models(self):
        return Model.objects(owner=self.id)