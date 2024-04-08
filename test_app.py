import unittest
from run import app  # Import your Flask app here

class SimpleTwitterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue('/login' in response.location)

    def test_registration_page(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Register', response.data)

    def test_login_page(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    # def test_user_registration(self):
    #     response = self.client.post('/register', data=dict(
    #         username='testuser',
    #         password='testpassword'
    #     ), follow_redirects=True)
    #     self.assertIn(b'Login', response.data)
    
    # def test_user_login(self):
    #     # Ensure you have a user to login with, might need to create one first.
    #     response = self.client.post('/login', data=dict(
    #         username='testuser',
    #         password='testpassword'
    #     ), follow_redirects=True)
    #     self.assertIn(b'Post a Chat', response.data)
    
    # Add more tests for posting chats, following users, etc.

if __name__ == '__main__':
    unittest.main()
