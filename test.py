__author__ = 'Jeremy Chen'

import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False # must set to False for unittest
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()
        self.add_user_to_database()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def add_user_to_database(self):
        new_user = User('jeremy', 'jeremy@gmail.com', 'jeremyateacher')
        db.session.add(new_user)
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'jeremy'

    def test_form_is_present(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please login to access your task list.', response.data)

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def register(self, name, email, password, confirm):
        response = self.app.post('/register/', data=dict(name=name, email=email, password=password, confirm=confirm),
                                 follow_redirects=True)
        return response

    def test_user_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password.', response.data)

    def test_user_can_login(self):
        response = self.login('jeremy', 'jeremyateacher')
        self.assertIn(b'Welcome', response.data)

    def test_user_can_register(self):
        response = self.register('justin', 'justin@justpython.com', 'justflask', 'justflask')
        self.assertIn(b'Thanks for registrering. Please login.', response.data )

    def test_duplicated_registration(self):
        response = self.register('justin', 'justin@justpython.com', 'justflask', 'justflask')
        response = self.register('justin', 'justin@justpython.com', 'justflask', 'justflask')
        self.assertIn(b'Username and/or email already exist.', response.data)

    def test_logged_in_user_can_logout(self):
        self.register('jerry', 'jerry@jerrypython.com', 'jerryflask', 'jerryflask')
        self.login('jerry', 'jerryflask')
        response = self.app.get('/logout/', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_user_cannot_logout(self):
        response = self.app.get('/logout/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_logged_in_user_can_access_tasks_page(self):
        self.login('jeremy', 'jeremyateacher')
        response = self.app.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_user_cannot_access_tasks_page(self):
        response = self.app.get('/tasks/', follow_redirects=True)
        self.assertIn(b'You need to login first.', response.data)

    def test_user_can_add_task(self):
        response = self.login_and_add_a_task()
        self.assertIn(b'New entry was successfully posted. Thanks.', response.data)

    def login_and_add_a_task(self, name='jeremy', password='jeremyateacher'):
        self.login(name, password)
        #self.app.get('/task/', follow_redirects=True)
        with self.app.session_transaction() as sess:
            user_id = sess['user_id']
            #print(user_id)
        new_task = dict(name='Go to the post office', due_date='31/12/2017', priority='1',
                        posted_date='01/12/2017', status='1', user_id=user_id)
        response = self.app.post('/add/', data=new_task, follow_redirects=True)
        return response

    def test_add_task_error(self):
        self.login('jeremy', 'jeremyateacher')
        self.app.get('/task/', follow_redirects=True)
        new_task = dict(name='Go to the post office', due_date='', priority='1',
                        posted_date='01/12/2017', status='1', user_id='1')
        response = self.app.post('/add/', data=new_task, follow_redirects=True)
        self.assertIn(b'This field is required.', response.data)

    def test_user_can_complete_task(self):
        self.login_and_add_a_task()
        response = self.app.get('/complete/1/', follow_redirects=True)
        self.assertIn(b'The task is complete. Nice', response.data)

    def test_user_can_delete_task(self):
        self.login_and_add_a_task()
        response = self.app.get('/delete/1/', follow_redirects=True)
        self.assertIn(b'The task was deleted.', response.data)

    def test_usr_can_only_complete_their_task(self):
        self.register('justin', 'justin@justpython.com', 'justflask', 'justflask')
        self.login('justin', 'justflask')
        self.login_and_add_a_task('justin', 'justflask')
        self.app.get('/logout/', follow_redirects=True)
        self.login_and_add_a_task()
        response = self.app.get('/complete/1/', follow_redirects=True)
        self.assertIn(b"You can&#39;t update other people&#39;s task.", response.data)

    def test_usr_can_only_delete_their_task(self):
        self.register('justin', 'justin@justpython.com', 'justflask', 'justflask')
        self.login('justin', 'justflask')
        self.login_and_add_a_task('justin', 'justflask')
        self.app.get('/logout/', follow_redirects=True)
        self.login_and_add_a_task()
        response = self.app.get('/delete/1/', follow_redirects=True)
        self.assertIn(b"You can&#39;t delete other people&#39;s task.", response.data)

if __name__ == '__main__':
    unittest.main()