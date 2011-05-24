from twisted.application.internet import TCPClient, TCPServer
from twisted.application.service import Application, MultiService
from twisted.internet.protocol import Factory
from twisted.python import log
from twisted.web.server import Site
from zombiepygman.web_api.urls import API

class ZombiePygManWebAPIService(MultiService):

    def __init__(self):
        MultiService.__init__(self)

        self.configure_services()

    def addService(self, service):
        MultiService.addService(self, service)

    def removeService(self, service):
        MultiService.removeService(self, service)

    def configure_services(self):

        #if section.startswith("world "):
        #    factory = BravoFactory(section[6:])
        #    server = TCPServer(factory.port, factory,
        #        interface=factory.interface)
        #    server.setName(factory.name)
        #    self.addService(server)
        #    self.factorylist.append(factory)

        factory = Site(API)
        port = 8000
        server = TCPServer(port, factory)
        server.setName("web")
        self.addService(server)

service = ZombiePygmanWebAPIService()

application = Application("ZombiePygman")
service.setServiceParent(application)
