from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.main import bp
from app.models import User, Project
from app.main.forms import SearchForm


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    projects = 
        Project.get_projects_created_by_username(current_user.username)
    
    return render_template("main/index.html", projects=projects)


@bp.route('/search/user', methods=['GET', 'POST'])
@login_required
def search_user():
    username = ''
    form = SearchForm()
    if form.validate_on_submit():
        username = form.name.data

    users = User.get_all(form.name.data) if username == '' \ 
                else User.get_user_by_username(username)
    
    return render_template("main/search.html", data=users, 
                            is_users=True, form=form)
                        

@bp.route('/search/project', methods=['GET', 'POST'])
@login_required
def search_project():
    projectname = ''
    form = SearchForm()
    if form.validate_on_submit():
        projectname = form.name.data

    projects = Project.get_all() if projectname == '' \ 
        else Project.get_project_by_name(projectname)
    
    return render_template("main/search.html", data=projects, 
                            is_users=False, form=form)

