from django.test import TestCase

from config import CONFIG

HOST_URL = CONFIG['HOST']['url']


class ViewsTestCase(TestCase):
    """Test views in users app"""
    def test_login_loads_properly(self):
        """The login page loads properly"""
        response = self.client.get(f'{HOST_URL}/users/login')
        self.assertEqual(response.status_code, 200)

    def test_signup_loads_properly(self):
        """The signup page loads properly"""
        response = self.client.get(f'{HOST_URL}/users/signup')
        self.assertEqual(response.status_code, 200)
