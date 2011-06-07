"""
Some really basic unit tests just to make sure we test all of our basic
code paths against obvious bugs and crashes.
"""
from unittest import TestCase
from zombiepygman.client import ZpmAPI
import config

class APITestCase(TestCase):
    """
    Base class for API test cases. Handles setting up a ZpmAPI object.
    """
    def setUp(self):
        self.api = ZpmAPI(security_token=config.API_SECURITY_TOKEN)

    def _test_for_success(self, result):
        self.assertTrue(result['success'])

class DataPlayerLocsTest(APITestCase):
    """
    /data/playerlocs
    """
    def test_basic(self):
        result = self.api.get_playerlocs()