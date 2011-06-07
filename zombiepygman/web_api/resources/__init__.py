"""
This JSON API is primarily used for executing Minecraft server commands from
a remote TCP connection. The :class:`APIResource` class is the top-level
entry in here where everything gets started from.
"""
from twisted.web.resource import NoResource
from zombiepygman.web_api.resource_utils import AuthenticationMixin
from zombiepygman.web_api.resources.commands import CmdPipingResource
from zombiepygman.web_api.resources.data import DataResource

class APIResource(AuthenticationMixin):
    """
    Top level

    Path: /
    """
    def getChild(self, path, request):
        if path == 'cmd':
            return CmdPipingResource()
        elif path == 'data':
            return DataResource()
        else:
            return NoResource()
