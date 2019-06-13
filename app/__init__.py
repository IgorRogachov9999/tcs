import os
from flask import Flask, request, current_app
from flask_login import LoginManager
from flask_moment import Moment
from flask_bootstrap import Bootstrap
from config import Config


bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    from app.error import bp as error_bp
    app.register_blueprint(error_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.project import bp as project_bp
    app.register_blueprint(project_bp)

    from app.user import bp as user_bp
    app.register_blueprint(user_bp)

    return app

from app import models
