"""
This JSON API is primarily used for executing Minecraft server commands from
a remote TCP connection. The :class:`APIResource` class is the top-level
entry in here where everything gets started from.

Quick path cheat-sheat
----------------------

* /cmd/listconnected - Connected player list.
* /cmd/stop - Stops the Minecraft server, and zombiepygman.
* /cmd/save-all - Runs a 'save-all'.
* /cmd/save-on - Enables auto-saving.
* /cmd/save-off - Disables auto-saving.
"""
from twisted.web.resource import NoResource
from twisted.web.server import NOT_DONE_YET
from zombiepygman.notchian_wrapper.process import NotchianProcess
from zombiepygman.web_api.resource_utils import JSONResourceMixin, PermissionDeniedResource, AuthenticationMixin, SimpleArgCommandResource

class CmdListConnected(JSONResourceMixin):
    """
    Lists connected players.

    Path: /cmd/listconnected

    JSON Response keys
    ------------------

    * player_list (list): The list of connected players.
    """
    def render_POST(self, request):
        """
        Responds to player list GET requests. The return value is a
        NOT_DONE_YET, which means the client will be kept waiting until we
        manually request.write() and request.finish() in the
        _player_list_callback().
        """
        # Pipes the 'list' command into the Minecraft server's stdin, adds
        # returns a deferred to add a callback to received the results.
        deferred_func = NotchianProcess.protocol.cmd_list_players()
        # Once we have the output from stdout, this callback is called, which
        # will request.write() and request.finish().
        deferred_func.addCallback(self._player_list_callback, request)
        # Wait until we manually finish the request in
        # the self._player_list_callback function.
        return NOT_DONE_YET

    def _player_list_callback(self, player_list, request):
        """
        Once we get the Connected players list from stdout, this callback is
        called. It will set the 'players_list' key in the JSON payload,
        and dump it back to the client via JSON.

        :param str player_list: The list of connected players, as it comes
            out of stdout.
        """
        self.context['player_list'] = player_list
        request.setHeader('Content-Type', 'application/json')
        request.write(self.get_context_json())
        # Un-block the client and return the result.
        request.finish()

class CmdStop(JSONResourceMixin):
    """
    Gracefully shuts down the server.

    Path: /cmd/stop
    """
    def get_context(self, request):
        """
        In this case, no context values are set, we just run the command. No
        output comes back from the command.
        """
        NotchianProcess.stop_minecraft_server()


class CmdSaveAll(JSONResourceMixin):
    """
    Runs a 'save-all'.

    Path: /cmd/save-all
    """
    def get_context(self, request):
        """
        In this case, no context values are set, we just run the command. No
        output comes back from the command.
        """
        NotchianProcess.protocol.send_mc_command('save-all')


class CmdSaveOn(JSONResourceMixin):
    """
    Runs a 'save-on'.

    Path: /cmd/save-on
    """
    def get_context(self, request):
        """
        In this case, no context values are set, we just run the command. No
        output comes back from the command.
        """
        NotchianProcess.protocol.send_mc_command('save-on')


class CmdSaveOff(JSONResourceMixin):
    """
    Runs a 'save-off'.

    Path: /cmd/save-off
    """
    def get_context(self, request):
        """
        In this case, no context values are set, we just run the command. No
        output comes back from the command.
        """
        NotchianProcess.protocol.send_mc_command('save-off')


class CmdKick(SimpleArgCommandResource):
    """
    Kicks the specified player.

    Path: /cmd/kick

    JSON Payload keys
    -----------------

    * player (str): The player to kick
    """
    command = 'kick'
    input_key = 'player'


class CmdBan(SimpleArgCommandResource):
    """
    Bans the specified player.

    Path: /cmd/ban

    JSON Payload keys
    -----------------

    * player (str): The player to ban
    """
    command = 'ban'
    input_key = 'player'


class CmdPardon(SimpleArgCommandResource):
    """
    Pardons the specified player.

    Path: /cmd/pardon

    JSON Payload keys
    -----------------

    * player (str): The player to pardon
    """
    command = 'pardon'
    input_key = 'player'


class CmdBanIP(SimpleArgCommandResource):
    """
    Bans the specified IP address.

    Path: /cmd/ban-ip

    JSON Payload keys
    -----------------

    * ip (str): The IP address to ban.
    """
    command = 'ban-ip'
    input_key = 'ip'


class CmdPardonIP(SimpleArgCommandResource):
    """
    Pardons the specified IP.

    Path: /cmd/pardon-ip

    JSON Payload keys
    -----------------

    * ip (str): The IP address to ban.
    """
    command = 'pardon-ip'
    input_key = 'ip'

        
class CmdPipingResource(AuthenticationMixin):
    """
    Wrapped commands

    Path: /cmd/*
    """
    # Maps the URL name to the resource.
    PATHS = {
        'listconnected': CmdListConnected,
        'stop': CmdStop,
        'save-all': CmdSaveAll,
        'save-on': CmdSaveOn,
        'save-off': CmdSaveOff,
        'kick': CmdKick,
        'ban': CmdBan,
        'pardon': CmdPardon,
        'ban-ip': CmdBanIP,
        'pardon-ip': CmdPardonIP,
    }

    def getChild(self, path, request):
        """
        Handles matching a URL path to an API method.

        :param str path: The URL path after /cmd/. IE: 'stop', 'save-all'.
        :rtype: Resource
        :returns: The Resource for the requested API method.
        """
        if not self._is_valid_security_token(request):
            return PermissionDeniedResource()

        # Check the PATHS dict for which resource should be returned for
        # any given path.
        resource = self.PATHS.get(path, None)
        if resource:
            # Instantiate the matching Resource child and return it.
            return resource()
        else:
            # No dict key matching the path was found. 404 it.
            return NoResource()


class APIResource(AuthenticationMixin):
    """
    Top level

    Path: /
    """
    def getChild(self, path, request):
        if path == 'cmd':
            return CmdPipingResource()
        else:
            return NoResource()
