"""
API calls that retrieve server/world data without directly interacting with
minecraft_server.jar's pty. For example, getting a player list from the
world dir, or finding player locations.
"""
import os
from nbt import NBTFile
from zombiepygman.web_api.resource_utils import JSONResourceMixin, SecuredRoutingResource
from zombiepygman.conf import settings

class DataPlayerLocs(JSONResourceMixin):
    """
    Returns a list of players and their locations. This API call operates in
    two different modes:

    * If a 'player_locs' key is set on the request dict and the value is
      a list, return the locations for the specified usernames.
    * If no 'player_locs' key is set, return all player locs found in
      world/players. If you have a large server, be careful about doing this!
      If you are extremely I/O bound and don't throttle this call, you are
      asking for trouble.

    .. warning: Make sure this call is only accessible to the website/app. There
        is very little here preventing all kinds of un-fun attacks.

    Response payload
    ----------------
    * player_locs - Top-level location dict. From within here, the keys are
        usernames (case-sensitive) in the form of::

        {
            'x': x.value,
            'y': y.value,
            'z': z.value,
            'yaw': yaw.value,
            'pitch': pitch.value,
        }

    Path: /data/playerlocs
    """
    def set_context(self, request):
        """
        Goes through the minecraft_server/world/players dir, retrieves one
        or more player locations. Returns in a JSON dict.
        """
        # world/players, should contain *.dat player data files.
        player_dir = os.path.join(
            settings.MINECRAFT_SERVER_DATA_DIR,
            'world',
            'players',
        )

        # Keys are case-sensitive usernames, values are a dict of loc data.
        player_locs = {}

        requested_players = self.user_input.get('for_players')
        if isinstance(requested_players, list):
            for username in requested_players:
                if '.' in username or '/' in username:
                    # TODO: Secure this up, you lazy fool.
                    continue

                nbt_file_name = '%s.dat' % username
                nbt_file_path = os.path.join(player_dir, nbt_file_name)

                try:
                    player_locs[username] = self._get_player_loc_data_from_nbt(
                        nbt_file_path)
                except IOError:
                    # Missing or otherwise un-readable player file.
                    continue

        else:
            for root, dirs, files in os.walk(player_dir):
                for file in files:
                    if not file.endswith('.dat'):
                        # This isn't an NBT file. Probably...
                        continue

                    nbt_file_path = os.path.join(player_dir, file)
                    # File name is case-correct.
                    username = file[:-4]
                    player_locs[username] = self._get_player_loc_data_from_nbt(
                                                nbt_file_path)

        # Sets the player location dict as the 'player_locs' key on the
        # JSON payload's top-level dict.
        self.context['player_locs'] = player_locs

    def _get_player_loc_data_from_nbt(self, nbt_file_path):
        """
        Opens a player NBT file, yanks the location data out, returns it
        in dict form for JSON serialization.

        :param str nbt_file_path: The full path to a player's .dat file.
        :rtype: dict
        :returns: A dict of player location data.
        """
        player = NBTFile(nbt_file_path)
        x, y, z = player['Pos'].tags
        yaw, pitch = player['Rotation'].tags

        return {
            'x': x.value,
            'y': y.value,
            'z': z.value,
            'yaw': yaw.value,
            'pitch': pitch.value,
        }


class DataResource(SecuredRoutingResource):
    """
    General server/world data.

    Path: /data/*
    """
    # Maps the URL name to the resource.
    PATHS = {
        'playerlocs': DataPlayerLocs,
    }