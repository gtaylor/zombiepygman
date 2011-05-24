from twisted.application.service import Application
from twisted.internet import reactor
from zombiepygman.web_api.service import ZombiePygManWebAPIService
from zombiepygman.notchian_wrapper.process import start_minecraft_server

application = Application("ZombiePygman")

# Set up the RESTful JSON API for interacting with the Minecraft server
# process. Goes through the transport set up later in this module.
service = ZombiePygManWebAPIService()
service.setServiceParent(application)

# Runs the java -jar minecraft_server.jar command in a separate process.
# Sets up a transport in notchian_wrapper.process.transport.
reactor.callWhenRunning(start_minecraft_server)