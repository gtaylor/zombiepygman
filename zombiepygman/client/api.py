"""
ZpmAPI is the main class that outside applications should go through to
make API calls. The public methods on ZpmAPI should all be of use, and
fairly obvious to anyone who has tinkered with minecraft_server.jar.
"""
from zombiepygman.client.api_backend import APIBackend

class ZpmAPI(APIBackend):
    """
    API calls should be sent through instances of this object. See
    zombiepygman.client.api_backend.APIBackend for instance attribs and
    possible config values.

    All return types are dicts unless otherwise noted.
    """
    def cmd_list_connected(self):
        """
        Returns a dict with a 'player_list' key that has a list of
        connected players.
        """
        return self._call_zpg_api('/cmd/listconnected')

    def cmd_save_all(self):
        """
        Forces a full save of world data.
        """
        return self._call_zpg_api('/cmd/save-all')
    
    def cmd_save_on(self):
        """
        Enables auto-saving.
        """
        return self._call_zpg_api('/cmd/save-on')


    def cmd_save_off(self):
        """
        Disables auto-saving.
        """
        return self._call_zpg_api('/cmd/save-off')

    def cmd_kick(self, player):
        """
        Kicks the given player.

        :param str player: The player to kick.
        """
        input = {'player': player}
        return self._call_zpg_api('/cmd/kick', payload=input)

    def cmd_ban(self, player):
        """
        Bans the given player.

        :param str player: The player to ban.
        """
        input = {'player': player}
        return self._call_zpg_api('/cmd/ban', payload=input)

    def cmd_pardon(self, player):
        """
        Pardons (un-bans) the given player.

        :param str player: The player to ban.
        """
        input = {'player': player}
        return self._call_zpg_api('/cmd/pardon', payload=input)