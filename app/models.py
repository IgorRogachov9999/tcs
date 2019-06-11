import psycopg2
from hashlib import md5
from time import time
from flask import g
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    if 'db' not in g:
        g.db = app.config['POSTGRESQL_POOL'].getconn()
    return g.db


class User():
    def __init__(self, username, email):
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
    def get_projects_where_username_is_manager(username):
        pass


    @staticmethod
    def get_all():
        pass
    

    @staticmethod
    def get_project_by_name(name):
        pass


    @staticmethod
    def get_projects_with_username(username):
        pass


    @staticmethod
    def get_projects_created_by_username(username):
        pass


class Task():
    def __init__(self):
        pass
    

    def save(self):
        pass


    @staticmethod
    def get_task_by_id(id):
        pass


    @staticmethod
    def get_username_tasks(username):
        pass


class Model():
    @staticmethod
    def rollback():
        pass