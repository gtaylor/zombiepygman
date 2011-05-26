"""
This JSON API is primarily used for executing Minecraft server commands from
a remote TCP connection. The :class:`APIResource` class is the top-level
entry in here where everything gets started from.

Quick path cheat-sheat
----------------------

* /cmd/listconnected - Connected player list.
"""
from twisted.web.resource import NoResource
from twisted.web.server import NOT_DONE_YET
from zombiepygman.notchian_wrapper.process import NotchianProcess
from zombiepygman.web_api.resource_utils import JSONResourceMixin, PermissionDeniedResource, AuthenticationMixin

class CmdListConnected(JSONResourceMixin):
    """
    Lists connected players.

    Path: /cmd/listconnected

    JSON Payload keys
    -----------------

    * player_list - The list of connected players.
    """
    def render_GET(self, request):
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


class CmdPipingResource(AuthenticationMixin):
    """
    Wrapped commands

    Path: /cmd/*
    """
    def getChild(self, path, request):
        if not self._is_valid_security_token(request):
            return PermissionDeniedResource()
        
        if path == 'listconnected':
            return CmdListConnected()
        else:
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
