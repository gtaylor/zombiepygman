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

class CmdListConnectedTest(APITestCase):
    """
    /cmd/listconnected
    """
    def test_basic(self):
        result = self.api.cmd_list_connected()
        self._test_for_success(result)
        self.assertEqual(True, isinstance(result['player_list'], list))


class CmdSaveAllTest(APITestCase):
    """
    /cmd/save-all
    """
    def test_basic(self):
        result = self.api.cmd_save_all()
        self._test_for_success(result)


class CmdSaveOffTest(APITestCase):
    """
    /cmd/save-off
    """
    def test_basic(self):
        result = self.api.cmd_save_off()
        self._test_for_success(result)


class CmdSaveOnTest(APITestCase):
    """
    /cmd/save-on
    """
    def test_basic(self):
        result = self.api.cmd_save_on()
        self._test_for_success(result)


class CmdKickTest(APITestCase):
    """
    /cmd/kick
    """
    def test_basic(self):
        result = self.api.cmd_kick('Snagglepants')
        self._test_for_success(result)


class CmdBanTest(APITestCase):
    """
    /cmd/ban
    """
    def test_basic(self):
        result = self.api.cmd_ban('Snagglepants')
        self._test_for_success(result)


class CmdPardonTest(APITestCase):
    """
    /cmd/pardon
    """
    def test_basic(self):
        result = self.api.cmd_pardon('Snagglepants')
        self._test_for_success(result)


class CmdBanIPTest(APITestCase):
    """
    /cmd/ban-ip
    """
    def test_basic(self):
        result = self.api.cmd_ban_ip('192.168.1.1')
        self._test_for_success(result)


class CmdPardonIPTest(APITestCase):
    """
    /cmd/pardon-ip
    """
    def test_basic(self):
        result = self.api.cmd_pardon_ip('192.168.1.1')
        self._test_for_success(result)