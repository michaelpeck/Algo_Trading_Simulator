import uuid
from src.common.database import Database
from src.models.calculation import Calculation
from src.models.strategy_model import Model
from flask import Flask, session

__author__ = 'michaelpeck'

class User(object):
    def __init__(self, first_name, last_name, email, password, user_id=None, _id=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.user_id = uuid.uuid4().hex if user_id is None else user_id
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users",{"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_id_by_email(cls, email):
        data = Database.find_one("users", {"email": email})
        if data is not None:
            return cls(**data)

    @classmethod
    def get_by_id(cls, user_id):
        data = Database.find_one("users", {"user_id": user_id})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email, password):
        user = User.get_by_email(email)
        if user is not None:
            return user.password == password
        return False

    @classmethod
    def register(cls, first_name, last_name, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(first_name, last_name, email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email

    @staticmethod
    def logout():
        session['email'] = None

    def get_entries(self):
        return Calculation.find_by_user_id(self.user_id)

    def get_models(self):
        return Model.find_by_user_id(self.user_id)

    def json(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "user_id": self.user_id,
            "password": self.password
        }
    def save_to_mongo(self):
        Database.insert("users", self.json())


    def get_id(self):
        return self.user_id