__author__ = 'michaelpeck'

import uuid
from src.common.database import Database
import datetime

class Post(object):

    def __init__(self, user_id, title, content, author, date=datetime.datetime.utcnow(), _id=None):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.author = author
        self.date = date
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def create_post(cls, user_id, title, content, author):
        new_post = cls(user_id, title, content, author)
        new_post.save_to_mongo()


    def save_to_mongo(self):
        Database.insert(collection='posts',data=self.json())

    def json(self):
        return{
            '_id': self._id,
            'user_id': self.user_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'date': self.date
        }

    @classmethod
    def from_mongo(cls, id):
        post_data = Database.find_one(collection='posts', query = {'_id': id})
        return cls(**post_data)


    @staticmethod
    def from_user(id):
        return [post for post in Database.find(collection = 'posts', query = {'user_id': id})]

    @staticmethod
    def all_posts():
        return [post for post in Database.find_all(collection='posts')]
