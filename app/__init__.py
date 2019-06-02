import os
from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_moment import Moment
from config import Config


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models
