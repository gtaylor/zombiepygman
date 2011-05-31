"""
Some really basic unit tests just to make sure we test all of our basic
code paths against obvious bugs and crashes.
"""
from unittest import TestCase
from zombiepygman.client import ZpmAPI

class APITestCase(TestCase):
    """
    Base class for API test cases. Handles setting up a ZpmAPI object.
    """
    def setUp(self):
        self.api = ZpmAPI()


class CmdListConnectedTest(APITestCase):
    """
    /cmd/listconnected
    """
    def test_basic(self):
        result = self.api.cmd_list_connected()
        self.assertEqual(True, isinstance(result['player_list'], list))


class CmdSaveAllTest(APITestCase):
    """
    /cmd/save-all
    """
    def test_basic(self):
        self.api.cmd_save_all()


class CmdSaveOffTest(APITestCase):
    """
    /cmd/save-off
    """
    def test_basic(self):
        self.api.cmd_save_off()


class CmdSaveOnTest(APITestCase):
    """
    /cmd/save-on
    """
    def test_basic(self):
        self.api.cmd_save_on()
