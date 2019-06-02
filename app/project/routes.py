from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app.project import bp
from app.project import User


@bp.route('/project/<projectname>', methods=['GET', 'POST'])
@login_required
def project(projectname):
    pass


@bp.route('/project/<projectname>/users', methods=['GET', 'POST'])
@login_required
def project_users(projectname):
    pass


@bp.route('/project/<projectname>/edit/<username>', methods=['GET', 'POST'])
@login_required
def project_users(projectname, username):
    pass


@bp.route('/project/<projectname>/tasks', methods=['GET', 'POST'])
@login_required
def project_tasks(projectname):
    pass


@bp.route('/task/<task>', methods=['GET', 'POST'])
@login_required
def task(task):
    pass




