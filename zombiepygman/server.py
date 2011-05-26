"""
The top-most bit of code that ties everything together into one runnable
server process. The two important parts here are:

* The RESTful JSON API that runs under twisted.web. This is primarily used
  to pipe commands into the Minecraft process from websites or other
  applications.
* The Minecraft server process whose stdin we can pipe commands into, and whose
  stdout we can monitor for activity.
"""
import sys
import os
from twisted.application.service import Application
from twisted.internet import reactor
from twisted.python import log
from zombiepygman.web_api.service import ZombiePygManWebAPIService
from zombiepygman.notchian_wrapper.process import NotchianProcess
from zombiepygman.conf import settings

# They need to set this to something, or we'll have a bunch of people running
# around with wide-open API servers.
if settings.API_SECURITY_TOKEN == None:
    log.err("ERROR: You have not set a new value for API_SECURITY_TOKEN in"\
            "your conf.py. Do that now, then start zombiepygman again.")
    log.err("ERROR: zombiepygman startup aborted.")
    sys.exit(1)

# The data dir holds server settings, the white-list, the world data, and etc.
if not os.path.exists(settings.MINECRAFT_SERVER_DATA_DIR):
    log.err("ERROR: The directory you specified in your "\
            "config.MINECRAFT_SERVER_DATA_DIR doesn't exist:")
    log.err("  %s" % settings.MINECRAFT_SERVER_DATA_DIR)
    sys.exit(1)

application = Application("ZombiePygman")

# Set up the RESTful JSON API for interacting with the Minecraft server
# process. Goes through the transport set up later in this module.
service = ZombiePygManWebAPIService()
service.setServiceParent(application)

# Runs the java -jar minecraft_server.jar command in a separate process.
# Sets up a transport in notchian_wrapper.process.transport.
reactor.callWhenRunning(NotchianProcess.start_minecraft_server)