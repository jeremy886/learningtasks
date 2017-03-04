__author__ = 'Jeremy Chen'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'learningtasks.db'
CSRF_ENABLED = True
SECRET_KEY = 'mysecret'

DATABASE_PATH = os.path.join(basedir, DATABASE)

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DATABASE_PATH