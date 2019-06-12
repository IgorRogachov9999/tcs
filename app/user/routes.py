from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from app.user import bp
from app.models import User, Project, Task
from app.user.forms import EditProfileForm


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
        return redirect(url_for('user.edit_profile'))
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


