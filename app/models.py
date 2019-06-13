import psycopg2
from hashlib import md5
from time import time
from flask import g
from enum import Enum
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


def get_db():
    if 'db' not in g:
        g.db = app.config['POSTGRESQL_POOL'].getconn()
    return g.db


def execute(query):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(query)
    answer = cursor.fetchall()
    cursor.close()
    return answer


def init_db():
    q = '''
        CREATE TABLE IF NOT EXISTS "User" ( 
            "id" serial NOT NULL, 
            "username" VARCHAR(255) NOT NULL UNIQUE, 
            "email" VARCHAR(255) NOT NULL UNIQUE, 
            "password" VARCHAR(255) NOT NULL, 
            "last_seen" integer NOT NULL, 
            CONSTRAINT "User_pk" PRIMARY KEY ("id") 
        ) WITH ( 
        OIDS=FALSE 
        ); 
        CREATE TABLE IF NOT EXISTS "User_Project_Role" (
            "user_id" integer NOT NULL,
            "project_id" integer NOT NULL,
            "role_id" integer NOT NULL,
            CONSTRAINT "User_Project_Role_pk" PRIMARY KEY ("user_id","project_id","role_id")
        ) WITH (
        OIDS=FALSE
        );
        CREATE TABLE IF NOT EXISTS "Project" (
            "id" serial NOT NULL,
            "name" VARCHAR(255) NOT NULL UNIQUE,
            "begin" integer NOT NULL,
            "description" TEXT NOT NULL,
            CONSTRAINT "Project_pk" PRIMARY KEY ("id")
        ) WITH (
        OIDS=FALSE
        );
        CREATE TABLE IF NOT EXISTS "Role" (
            "id" integer NOT NULL,
            "role" VARCHAR(255) NOT NULL UNIQUE,
            CONSTRAINT "Role_pk" PRIMARY KEY ("id")
        ) WITH (
        OIDS=FALSE
        );
        CREATE TABLE IF NOT EXISTS "Task" (
            "id" serial NOT NULL,
            "description" TEXT NOT NULL,
            "user" integer NOT NULL,
            "project" integer NOT NULL,
            "status" integer NOT NULL,
            "start" integer NOT NULL,
            "deathline" integer NOT NULL,
            CONSTRAINT "Task_pk" PRIMARY KEY ("id")
        ) WITH (
        OIDS=FALSE
        );
        CREATE TABLE IF NOT EXISTS "Status" (
            "id" integer NOT NULL,
            "status" VARCHAR(255) NOT NULL,
            CONSTRAINT "Status_pk" PRIMARY KEY ("id")
        ) WITH (
        OIDS=FALSE
        );
        ALTER TABLE "User_Project_Role" ADD CONSTRAINT "User_Project_Role_fk0" FOREIGN KEY ("user_id") REFERENCES "User"("id");
        ALTER TABLE "User_Project_Role" ADD CONSTRAINT "User_Project_Role_fk1" FOREIGN KEY ("project_id") REFERENCES "Project"("id");
        ALTER TABLE "User_Project_Role" ADD CONSTRAINT "User_Project_Role_fk2" FOREIGN KEY ("role_id") REFERENCES "Role"("id");
        ALTER TABLE "Task" ADD CONSTRAINT "Task_fk0" FOREIGN KEY ("user") REFERENCES "User"("id");
        ALTER TABLE "Task" ADD CONSTRAINT "Task_fk1" FOREIGN KEY ("project") REFERENCES "Project"("id");
        ALTER TABLE "Task" ADD CONSTRAINT "Task_fk2" FOREIGN KEY ("status") REFERENCES "Status"("id");
        INSERT INTO "Role" (id, role) VALUES ({0}, \'DEVELOPER\');
        INSERT INTO "Role" (id, role) VALUES ({1}, \'MANAGER\');
        INSERT INTO "Role" (id, role) VALUES ({2}, \'CREATOR\');
        INSERT INTO "Status" (id, role) VALUES ({3}, \'IN_PROCESS\');   
        INSERT INTO "Status" (id, role) VALUES ({4}, \'DONE\');
        '''.format(Role.DEVELOPER, Role.MANAGER, Role.CREATOR, Status.IN_PROCESS, Status.DONE)
    
    execute(q)
        

class Role(Enum):
    DEVELOPER = 1
    MANAGER = 2
    CREATOR = 3


class Status(Enum):
    IN_PROCESS = 1
    DONE = 2


class User(UserMixin):
    def __init__(self, username, email):
        self.id = 0
        self.username = username
        self.email = email
        self.password = ""
        self.last_seen = time()

    
    def __init__(self, id, username, email, password, last_seen):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.last_seen = last_seen


    def set_password(self, password):
        self.password = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password, password)

    
    def save(self):
        q = 'INSERT INTO \"User\" (username, email, password, last_seen)' \
            " VALUES ('{0}', '{1}', '{2}', {3});".format(
            self.username,
            self.email,
            self.password,
            self.last_seen
        )
        execute(query)


    def update(self):
        q = "UPDATE \"User\" SET username = '{0}', email = '{1}', " \ 
            "password = '{2}', last_seen = {3} WHERE id = {5};".format(
            self.username,
            self.email,
            self.password,
            self.last_seen,
            self.id
        )
        execute(query)


    @staticmethod
    def get_user_by_id(id):
        q = 'SELECT * FROM \"User\" WHERE id = {0};'.format(id)
        res = execute(query)
        return User(*res[0]) if len(res) != 0 else None


    @staticmethod
    def get_all():
        q = 'SELECT * FROM \"User\";'
        res = execute(q)
        return [User(*u) for u in res]


    @staticmethod
    def get_user_by_username(username):
        q = "SELECT * FROM \"User\" WHERE username = '{0}';".format(username)
        res = execute(q)
        return User(*res[0]) if len(res) != 0 else None


    @staticmethod
    def get_user_by_email(email):
        q = "SELECT * FROM \"User\" WHERE email = '{0}';".format(email)
        res = execute(q)
        return User(*res[0]) if len(res) != 0 else None


    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


@login.user_loader
def load_user(id):
    return User.get_user_by_id(id)


class Project():
    def __init__(self, name, description):
        self.id = 0
        self.name = name
        self.description = description
        self.begin = time()


    def __init__(self, id, name, description, begin):
        self.id = id
        self.name = name
        self.description = description
        self.begin = begin


    def save(self):
        q = "INSERT INTO \"Project\" (name, description, begin) " \
            "VALUES ('{0}', '{1}', {2});".format(
                self.name,
                self.description,
                self.begin
            )
        execute(query)


    @staticmethod
    def get_project_users(project_id):
        q = "SELECT id, username, email, password, last_seen FROM " \
            "\"User_Project_Role\" LEFT JOIN \"User\"" \
            " ON \"User_Project_Role\".user_id = \"User\".id " \
            "WHERE project_id = {0};".format(project_id)
        res = execute(q)
        return [User(*u) for u in res]


    @staticmethod
    def set_user_role(project_id, user_id, role):
        q = "SELECT * FROM \"User_Project_Role\" WHERE " \
             "user_id = {0} AND project_id = {1};".format(
                 user_id,
                 project_id
             )
        res = exec(q)
        if len(res) == 0:
            q = "INSERT INTO \"User_Project_Role\"" \
                " (user_id, project_id, role_id) VALUES (" \
                " {0}, {1}, {2});".format(
                    user_id,
                    project_id,
                    role
                )
        else:
            q = "UPDATE \"User_Project_Role\" SET role_id = '{0}' " \
                "WHERE user_id = {1} AND project_id = {2};".format(
                    role,
                    user_id,
                    project_id
                )
        execute(q)
    
    @staticmethod
    def add_user_to_project(user_id, project_id):
        q = "SELECT * FROM \"User_Project_Role\" WHERE " \
             "user_id = {0} AND project_id = {1};".format(
                 user_id,
                 project_id
             )
        res = execute(q)
        if len(res) == 0:
            q = "INSERT INTO \"User_Project_Role\"" \
                " (user_id, project_id, role_id) VALUES (" \
                " {0}, {1}, {2});".format(
                    user_id,
                    project_id,
                    Role.DEVELOPER
                )
            execute(q)


    @staticmethod
    def get_projects_where_username_is_manager(username):
        id = User.get_user_by_username(username).id
        q = "SELECT id, name, description, begin FROM " \
            "\"User_Project_Role\" LEFT JOIN \"Project\"" \
            " ON \"User_Project_Role\".project = \"Project\".id " \
            "WHERE user_id = {0} AND role_id = {1};".format(
                id,
                Role.MANAGER
            )
        res = execute(q)
        return [Project(*p) for p in res]


    @staticmethod
    def get_all():
        q = "SELECT * FROM \"Project\";"
        res = execute(q)
        return [Project(*p) for p in res]

    @staticmethod
    def get_user_role(project_id, user_id):
        q = "SELECT role_id FROM \"User_Project_Role\" WHERE " \
            "project_id = {0} AND user_id = {1};".format(
                project_id,
                user_id
            )
        res = execute(q)
        return res[0][0] if len(res) != 0 else None


    @staticmethod
    def get_project_by_name(name):
        q = 'SELECT * FROM "Project" WHERE name = {0};'.format(name)
        res = execute(q)
        return None if len(res) == 0 else Project(*res[0])

    
    @staticmethod
    def get_project_by_id(project_id):
        q = 'SELECT * FROM "Project" WHERE id = {0};'.format(project_id)
        res = execute(q)
        return None if len(res) == 0 else Project(*res[0])


    @staticmethod
    def get_project_users_and_rols(prjectname):
        q = "SELECT id, username, email, password, last_seen, role_id FROM " \
            "\"User_Project_Role\" LEFT JOIN \"User\"" \
            " ON \"User_Project_Role\".user_id = \"User\".id " \
            "WHERE project_id = {0};".format(project_id)
        res = execute(q)
        answer = [{'user': User(*line[:-1]), 'role': line[-1]} for line in res]
        return answer


    @staticmethod
    def get_projects_with_username(username):
        id = User.get_user_by_username(username).id
        q = "SELECT id, name, description, begin FROM " \
            "\"User_Project_Role\" LEFT JOIN \"Project\"" \
            " ON \"User_Project_Role\".project_id = \"Project\".id " \
            "WHERE user_id = {0};".format(id)
        res = execute(q)
        return [Project(*p) for p in res]


    @staticmethod
    def get_projects_created_by_username(username):
        id = User.get_user_by_username(username).id
        q = "SELECT id, name, description, begin FROM " \
            "\"User_Project_Role\" LEFT JOIN \"Project\"" \
            " ON \"User_Project_Role\".project_id = \"Project\".id " \
            "WHERE user_id = {0} AND role_id = {1};".format(id, Role.CREATOR)
        res = execute(q)
        return [Project(*p) for p in res]

    
    @staticmethod
    def get_creator(projectname):
        id = Project.get_project_by_name(projectname).id
        q = 'SELECT user_id FROM "User_Project_Role" WHERE ' \
            'project_id = {0} AND role_id = {1}'.format(id, Role.CREATOR)
        res = execute(q)
        return User.get_user_by_id(res[0][0])


class Task():
    def __init__(self, id=0, description, user, project, 
                 status=Status.IN_PROCESS, deathline, start=time()):
        self.id = id
        self.description = description
        self.user = user
        self.project = project
        self.status = status
        self.deathline = deathline
        self.start = start


    def save(self):
        q = "INSERT INTO \"Task\" (description, user, project, status, " \
            "deathline, start) VALUES ('{0}', '{1}', {2}, {3}, {4}, {5});" \
            .format(
                self.description,
                self.user,
                self.project,
                self.status,
                self.deathline
                self.start
            )
        execute(query)

    def update(self):
        q = "UPDATE \"Task\" SET description = {0}, user = {1}, " \ 
            "project = {2}, status = {3}, deathline = {4}, start = {5} " \
            "WHERE id = {6};" \
            .format(
                self.description,
                self.user,
                self.project,
                self.status,
                self.deathline
                self.start,
                self.id
            )
        execute(query)


    @staticmethod
    def get_task_by_id(id):
        q = 'SELECT * FROM "Task" WHERE id = {0};'.format(id)
        res = execute(q)
        return None if len(res) == 0 else Task(*res[0])


    @staticmethod
    def get_username_tasks(username):
        id = User.get_user_by_username(username)
        q = 'SELECT * FROM "Task" WHERE user = {0};'.format(id)
        res = execute(q)
        return [Task(*t) for t in res]

    
    @staticmethod
    def get_tasks_by_project_id(project_id):
        q = 'SELECT * FROM "Task" WHERE project = {0};'.format(id)
        res = execute(q)
        return [Task(*t) for t in res]


class Model():
    @staticmethod
    def rollback():
        raise NotImplementedError