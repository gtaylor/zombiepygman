from twisted.internet import protocol, defer
from zombiepygman.notchian_wrapper.unsafe_store import PlayerListStore

class NotchianProcessProtocol(protocol.ProcessProtocol):
    """
    Used to communicate with the Minecraft server process.
    """
    def __init__(self, *args, **kwargs):
        self.outbuffer = ''
        self._waiting = []

    def errReceived(self, data):
        print "stderr: %s" % data

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

    def listPlayers(self):
        self.transport.write("list\n")
        self._waiting.append(defer.Deferred())
        return self._waiting[-1]

    def parseLines(self, data):
        return data.strip().split('\r\n')

    def outReceived(self, bytes):
        outbuffer = self.outbuffer + bytes
        #lines, leftover = self.parseLines(outbuffer)
        #lines, leftover = self.parseLines(outbuffer)
        lines = self.parseLines(outbuffer)
        #self.outbuffer = leftover

        for line in lines:
            if '[INFO] Connected players:' in line:
                self._waiting.pop(0).callback(line)