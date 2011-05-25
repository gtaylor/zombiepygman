"""
The top-most bit of code that ties everything together into one runnable
server process. The two important parts here are:

* The RESTful JSON API that runs under twisted.web. This is primarily used
  to pipe commands into the Minecraft process from websites or other
  applications.
* The Minecraft server process whose stdin we can pipe commands into, and whose
  stdout we can monitor for activity.
"""
from twisted.application.service import Application
from twisted.internet import reactor
from zombiepygman.web_api.service import ZombiePygManWebAPIService
from zombiepygman.notchian_wrapper.process import NotchianProcess

application = Application("ZombiePygman")

# Set up the RESTful JSON API for interacting with the Minecraft server
# process. Goes through the transport set up later in this module.
service = ZombiePygManWebAPIService()
service.setServiceParent(application)

# Runs the java -jar minecraft_server.jar command in a separate process.
# Sets up a transport in notchian_wrapper.process.transport.
reactor.callWhenRunning(NotchianProcess.start_minecraft_server)