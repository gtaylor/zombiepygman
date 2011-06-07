"""
Quick path cheat-sheat
----------------------

* /data/playerlocs - Get a list of player locations.
"""
from twisted.web.resource import NoResource
from zombiepygman.web_api.resource_utils import JSONResourceMixin, PermissionDeniedResource, AuthenticationMixin

class DataPlayerLocs(JSONResourceMixin):
    """
    Returns a list of players and their locations.

    Path: /data/playerlocs
    """
    def get_context(self, request):
        print "YAY"


class DataResource(AuthenticationMixin):
    """
    General server/world data.

    Path: /data/*
    """
    # Maps the URL name to the resource.
    PATHS = {
        'playerlocs': DataPlayerLocs,
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
        resource = self.PATHS.get(path)
        if resource:
            # Instantiate the matching Resource child and return it.
            return resource()
        else:
            # No dict key matching the path was found. 404 it.
            return NoResource()