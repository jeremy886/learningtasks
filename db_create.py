__author__ = 'Jeremy Chen'

import sqlite3

from _config import DATABASE_PATH

with sqlite3.connect(DATABASE_PATH) as conn:
    c = conn.cursor()
    c.execute('''CREATE TABLE tasks ( task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    due_date TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    status INTEGER NOT NULL)''')
    c.execute('INSERT INTO tasks (name, due_date, priority, status)'
              'VALUES("Finish this tutorial", "25/03/2017", 10, 1)')
    c.execute('INSERT INTO tasks (name, due_date, priority, status)'
              'VALUES("Finish Coursera Data Science Course", "15/04/2017", 10, 1)')