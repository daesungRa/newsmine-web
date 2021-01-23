from django.test import TestCase

from config import CONFIG

HOST_URL = CONFIG['HOST']['url']


class ViewsTestCase(TestCase):
    """Test views in core app"""
    def test_home_loads_properly(self):
        """The home page loads properly"""
        response = self.client.get(HOST_URL)
        self.assertEqual(response.status_code, 200)
