__author__ = 'Jeremy Chen'

from views import db
from models import Task
from datetime import date, datetime

from _config import DATABASE_PATH

db.create_all()

db.session.add(Task('Finish this tutorial', date(2016, 9, 22), 10, datetime.utcnow(), 1, 1))
db.session.add(Task('Finish Week 5 Lesson Plan', date(2017, 3, 25), 10, datetime.utcnow(), 1, 1))

db.session.commit()