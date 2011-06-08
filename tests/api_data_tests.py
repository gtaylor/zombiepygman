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
        """
        Just run through the code path to make sure we're exceptionless.
        """
        result = self.api.get_playerlocs()
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['player_locs'], dict)

    def test_invalid_username(self):
        """
        Given completely BS username(s), an empty dict value will be returned.
        Match-less usernames will fail silently.
        """
        players = ['blartyblartfast', 'someotherguy']
        result = self.api.get_playerlocs(for_players=players)
        self.assertIsInstance(result, dict)
        self.assertEqual({}, result['player_locs'])
