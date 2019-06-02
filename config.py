import os
from psycopg2 import pool

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'key'
    POSTGRESQL_POOL = os.environ.get('POSTGRESQL_POOL') or \
        pool.SimpleConnectionPool(1, 20, user='igor', password='123',
                                  host='127.0.0.1', port='5432',
                                  database='kurs')
                                 

