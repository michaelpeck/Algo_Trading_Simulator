__author__ = 'michaelpeck'

from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from src.config import Config
from src.common.database import Database

sqldb = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    sqldb.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

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
        Database.initialize()
        session['email'] = None

    return app