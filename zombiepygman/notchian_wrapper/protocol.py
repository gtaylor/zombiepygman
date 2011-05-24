from twisted.internet import protocol

class NotchianProcessProtocol(protocol.ProcessProtocol):
    """
    Used to communicate with the Minecraft server process.
    """
    def outReceived(self, data):
        print "stdout:", data

    def errReceived(self, data):
        print "stderr:", data

    def inConnectionLost(self):
        print "inConnectionLost! stdin is closed! (we probably did it)"

    def errConnectionLost(self):
        print "errConnectionLost! The child closed their stderr."

    def processExited(self, reason):
        print "processExited, status %d" % (reason.value.exitCode,)

    def processEnded(self, reason):
        print "processEnded, status %d" % (reason.value.exitCode,)
        print "quitting"
        #reactor.stop()