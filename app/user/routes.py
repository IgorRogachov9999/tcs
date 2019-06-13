from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.user import bp
from app.models import User, Project, Task
from app.user.forms import EditProfileForm, AddToProjectForm, \
                           CreateProjectForm


@bp.route('/user/<username>')
@login_required
def profle(username):
    user = User.get_user_by_username(username)
    if user is None:
        return redirect(url_for('error.not_found_error'))
    return render_template('user/profile.html', user=user)


@bp.route('/user/edit/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.update()
        flash('Your changes have been saved!')
        return redirect(url_for('user.edit_profile', user=user))
    return render_template('user/edit.html', title='Edit',
                           form=form) 


@bp.route('/user/<username>/projects')
@login_required
def user_projects(username):
    projects = Project.get_projects_with_username(username)
    return render_template('user/projects.html', title=username+' projects',
                            projects=projects)


@bp.route('/user/<username>/tasks')
@login_required
def user_tasks(username):
    tasks = Task.get_username_tasks(username)
    return render_template('user/tasks.html', title=username+' tastks',
                            tasks=tasks)


@bp.route('/user/<username>/add/<projectname>', methods=['GET', 'POST'])
@login_required
def add_to_project(username, projectname):
    user = User.get_user_by_username(username)
    if user is None:
        return redirect(url_for('error.not_found_error'))
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    user_projects = Project.get_projects_where_username_is_manager(
                    current_user.username)
    form = AddToProjectForm()
    form.project.choices = [(project.id, project.name) \
                                for project in user_projects]
    if form.validate_on_submit():
        Project.add_user_to_project(user.id, project.id)
        return redirect(url_for('user.profile', user=user))
    return render_template('user/add_to_project.html', title='Edit',
                           form=form) 


@bp.route('/user/project/create', methods=['GET', 'POST'])
@login_required
def create_project():
    form = CreateProjectForm()
    if form.validate_on_submit():
        project = Project(form.name.data,
                          form.description.data)
        project.save()
        return redirect(url_for("user.profile", user=user))
    return render_template("user/create_project.html", form=form)