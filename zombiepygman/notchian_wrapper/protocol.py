from twisted.internet import protocol

class NotchianProcessProtocol(protocol.ProcessProtocol):
    """
    Used to communicate with the Minecraft server process.
    """
    def outReceived(self, data):
        print data
        #log.msg(data)

    def errReceived(self, data):
        print data
        #log.err(data)