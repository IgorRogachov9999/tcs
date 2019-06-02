from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app.main import bp
from app.models import User


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    pass


@bp.route('/search/user/<username>')
@login_required
def search_user(username):
    pass


@bp.route('/search/project/<projectname>')
@login_required
def search_project(projectname):
    pass

