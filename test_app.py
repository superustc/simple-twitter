import unittest
from unittest.mock import patch

with patch.dict('os.environ', {'SIMPLE_TWITTER_DATABASE_URI': 'sqlite://'}):
    from run import app

from simple_twitter import db
from simple_twitter.models import Chat, User


class SimpleTwitterTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        with app.app_context():
            db.create_all()
        self.addCleanup(self.drop_tables)

    def drop_tables(self):
        with app.app_context():
            db.drop_all()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

    def test_registration_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_authenticated_user_can_post_chat(self):
        credentials = {'username': 'testuser', 'password': 'test-password'}
        response = self.client.post('/register', data=credentials)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/login')
        response = self.client.post('/login', data=credentials)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/')

        with app.app_context():
            # The old route rolled back after a successful commit, masking its
            # AttributeError. Checking only the persisted row misses that bug.
            with patch.object(db.session, 'rollback', wraps=db.session.rollback) as rollback:
                response = self.client.post('/post_chat', data={'content': 'Hello'})
            self.assertEqual(response.status_code, 302)
            self.assertEqual(response.location, '/')
            chat = Chat.query.one()
            self.assertEqual(chat.content, 'Hello')
            self.assertEqual(chat.user_id, User.query.filter_by(username='testuser').one().id)
            rollback.assert_not_called()


if __name__ == '__main__':
    unittest.main()
