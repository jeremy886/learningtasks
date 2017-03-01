__author__ = 'Jeremy Chen'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = 'learningtasks.db'
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'mysecret'

DATABASE_PATH = os.path.join(basedir, DATABASE)