"""
Quick path cheat-sheat
----------------------

* /data/playerlocs - Get a list of player locations.
"""
from zombiepygman.web_api.resource_utils import JSONResourceMixin, SecuredRoutingResource

class DataPlayerLocs(JSONResourceMixin):
    """
    Returns a list of players and their locations.

    Path: /data/playerlocs
    """
    def get_context(self, request):
        print "YAY"


class DataResource(SecuredRoutingResource):
    """
    General server/world data.

    Path: /data/*
    """
    # Maps the URL name to the resource.
    PATHS = {
        'playerlocs': DataPlayerLocs,
    }