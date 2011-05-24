from twisted.application.service import MultiService
from twisted.application.internet import TCPServer
from twisted.web.server import Site
from zombiepygman.web_api.urls import API

class ZombiePygManWebAPIService(MultiService):
    """
    Runs a RESTful JSON API, used to interact with the Minecraft server that
    is being wrapped.
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
        factory = Site(API)
        port = 8000
        server = TCPServer(port, factory)
        server.setName("web")
        self.addService(server)