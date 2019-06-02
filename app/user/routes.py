from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app.user import bp
from app.models import User

@bp.route('/user/<username>')
@login_required
def profle(username):
    pass


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    pass


@bp.route('/user/<username>/projects')
@login_required
def user_projects(username):
    pass


@bp.route('/user/<username>/tasks')
@login_required
def user_tasks(username):
    pass


@bp.route('/user/<username>/tasks/<projectname>')
@login_required
def user_project_tasks(username, projectname):
    pass


