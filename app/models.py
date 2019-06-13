import psycopg2
from hashlib import md5
from time import time
from flask import g
from enum import Enum
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    if 'db' not in g:
        g.db = app.config['POSTGRESQL_POOL'].getconn()
    return g.db


class User():
    def __init__(self, username, email):
        self.id = 0
        self.username = username
        self.email = email
        self.password = ""
        self.last_seen = time()

    
    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)

    
    def save(self):
        pass


    def update(self):
        pass


    @staticmethod
    def get_all():
        pass


    @staticmethod
    def get_user_by_username(username):
        pass
    

    @staticmethod
    def get_user_by_email(email):
        pass


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Project():
    def __init__(self, name, creator, description):
        self.id = 0
        self.name = name
        self.creator = creator
        self.description = description
        self.begin = time()


    def save(self):
        pass


    @staticmethod
    def get_project_users(project_id):
        pass


    @staticmethod
    def set_user_role(project_id, user_id, role):
        pass

    
    @staticmethod
    def add_user_to_project(user_id, project_id):
        pass


    @staticmethod
    def get_projects_where_username_is_manager(username):
        pass


    @staticmethod
    def get_all():
        pass
    

    @staticmethod
    def get_user_role(project_id, user_id):
        pass


    @staticmethod
    def get_project_by_name(name):
        pass

    
    @staticmethod
    def get_project_by_id(project_id):
        pass


    @staticmethod
    def get_project_users_and_rols(prjectname):
        pass


    @staticmethod
    def get_projects_with_username(username):
        pass


    @staticmethod
    def get_projects_created_by_username(username):
        pass

    
    @staticmethod
    def get_creator(projectname):
        pass


class Task():
    def __init__(self, description, user, project, deathline):
        self.description = description
        self.user = user
        self.project = project
        self.status = Status.IN_PROCESS
        self.deathline = deathline
        self.start = time()
    

    def save(self):
        pass


    @staticmethod
    def get_task_by_id(id):
        pass


    @staticmethod
    def get_username_tasks(username):
        pass

    
    @staticmethod
    def get_tasks_by_project_id(project_id):
        pass


class Role(Enum):
    DEVELOPER = 1
    MANAGER = 2
    CREATOR = 3


class Status(Enum):
    IN_PROCESS = 1
    DONE = 2


class Model():
    @staticmethod
    def rollback():
        pass