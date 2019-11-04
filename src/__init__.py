__author__ = 'michaelpeck'

from flask import Flask, session
from flask_login import LoginManager
from flask_mail import Mail
from src.config import Config
from src.common.database import Database
from flask_mongoengine import MongoEngine, Document

db = MongoEngine()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    from src.main.routes import main
    from src.users.routes import users
    from src.posts.routes import posts
    from src.processes.routes import processes
    from src.errors.handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(processes)
    app.register_blueprint(errors)

    @app.before_first_request
    def initialize_database():
        Database.initialize(Config)
        session['email'] = None

    return app