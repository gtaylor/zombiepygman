from twisted.application.internet import TCPClient, TCPServer
from twisted.application.service import Application, MultiService
from twisted.internet import protocol
from twisted.internet import reactor
from twisted.python import log

from twisted.web.server import Site
from zombiepygman.web_api.urls import API

class NotchianProcessProtocol(protocol.ProcessProtocol):

    def outReceived(self, data):
        print data
        #log.msg(data)

    def errReceived(self, data):
        print data
        #log.err(data)

class ZombiePygManWebAPIService(MultiService):

    def __init__(self):
        MultiService.__init__(self)

        self.configure_services()

    def addService(self, service):
        MultiService.addService(self, service)

    def removeService(self, service):
        MultiService.removeService(self, service)

    def configure_services(self):

        factory = Site(API)
        port = 8000
        server = TCPServer(port, factory)
        server.setName("web")
        self.addService(server)

application = Application("ZombiePygman")

service = ZombiePygManWebAPIService()
service.setServiceParent(application)



def whenRunning():
    notchian_proto = NotchianProcessProtocol()
    transport = reactor.spawnProcess(
    notchian_proto, "/usr/bin/java",
        [
            "blarty",
            "-jar",
            "/Users/gtaylor/Documents/workspace/zombiepygman/minecraft_server.jar",
            "nogui"
        ], {}
    )
reactor.callWhenRunning(whenRunning)