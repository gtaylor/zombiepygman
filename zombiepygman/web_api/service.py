"""
RESTful API service instantiation.
"""
from twisted.application.service import MultiService
from twisted.application.internet import TCPServer
from twisted.web.server import Site
from zombiepygman.web_api.resources import APIResource

class ZombiePygManWebAPIService(MultiService):
    """
    Runs a RESTful JSON API, primarily used to pipe commands into the
    Minecraft server's interactive shell via a remote TCP connection.
    """
    def __init__(self):
        MultiService.__init__(self)

        self.configure_service()

    def addService(self, service):
        MultiService.addService(self, service)

    def removeService(self, service):
        MultiService.removeService(self, service)

    def configure_service(self):
        """
        Instantiation and startup for the RESTful API.
        """
        root = APIResource()
        factory = Site(root)
        
        # TODO: Make this configurable.
        port = 8000
        server = TCPServer(port, factory)
        server.setName("web")
        self.addService(server)