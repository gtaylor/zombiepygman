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
    Returns a list of players and their locations.

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