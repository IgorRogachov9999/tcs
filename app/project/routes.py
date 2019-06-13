from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import current_user, login_required
from app.project import bp
from app.models import User, Project, Task, Role, Status
from app.project.forms import ManagerForm, AddTaskForm, SetTaskDoneForm


@bp.route('/project/<projectname>')
@login_required
def project(projectname):
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    creator = Project.get_creator(projectname)
    return render_template("project/project.html", project=project,
                            creator=creator)


@bp.route('/project/<projectname>/users')
@login_required
def project_users(projectname):
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    users_and_roles = Project.get_project_users_and_rols(projectname)
    return render_template("project/user_list.html", 
                            users_and_roles=users_and_roles)
    

@bp.route('/project/<projectname>/edit/<username>', methods=['GET', 'POST'])
@login_required
def project_user(projectname, username):
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    current_user_role = Project.get_user_role(project.id, current_user.id)
    if current_user_role is None or current_user_role == Role.DEVELOPER:
        return redirect(url_for('project.project_users', 
                                 projectname=projectname))
    user = User.get_user_by_username(username)
    if user is None:
        return redirect(url_for('error.not_found_error'))
    role = Project.get_user_role(project.id, user.id)
    if user.id == current_user.id or role == Role.CREATOR:
        return redirect(url_for("project_users", projectname))
    form = ManagerForm()
    if form.validate_on_submit():
        Project.set_user_role(project.id, user.id, form.manager.data)
    return render_template("project/project_user.html",
                            user=user, role=role, form=form)


@bp.route('/project/<projectname>/tasks', methods=['GET', 'POST'])
@login_required
def project_tasks(projectname):
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    tasks = Task.get_tasks_by_project_id(project.id)
    return render_template("project/tasks.html", tasks=tasks)


@bp.route('/task/<task>', methods=['GET', 'POST'])
@login_required
def task(task):
    current_task = Task.get_task_by_id(task)
    if current_task is None:
        return redirect(url_for('error.not_found_error'))
    form = SetTaskDoneForm()
    if form.validate_on_submit():
        current_user.status = Status.DONE
        current_task.update()
    return render_template("project/task.html", task=current_task
                            form=form)


@bp.route('/task/add/<projectname>', methods=['GET', 'POST'])
@login_required
def add_task(projectname):
    project = Project.get_project_by_name(projectname)
    if project is None:
        return redirect(url_for('error.not_found_error'))
    role = Project.get_user_role(project.id, current_user.id)
    if role is None or role == Role.DEVELOPER:
        return redirect(url_for("main.index"))
    form = AddTaskForm()
    project_users = Project.get_project_users(project.id)
    form.user.choices = [(user.id, user.username) for user in project_users]
    if form.validate_on_submit():
        task = Task(form.description.data,
                    form.user.data,
                    project.id,
                    form.user.data,
                    form.deathline.data)
        task.save()
        return redirect(url_for("main.index"))
    return render_template("project/add_task.html", form=form)




