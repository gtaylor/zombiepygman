"""
The protocol for communicating with the running Minecraft process.
"""
import datetime
from twisted.python import log
from twisted.internet import protocol, defer, reactor

class NotchianProcessProtocol(protocol.ProcessProtocol):
    """
    Used to communicate with the Minecraft server process. Any communication
    directly to/from the Minecraft process should be done in here.
    """
    def __init__(self, *args, **kwargs):
        # Stuff waiting to be parsed.
        self.outbuffer = ''
        # A stack of defer.Deferred objects to be used for sending the
        # result of the 'list' command to the API user.
        self._player_list_deferreds = []

    def errReceived(self, data):
        print "stderr: %s" % data

    def inConnectionLost(self):
        log.err("inConnectionLost! stdin is closed! (we probably did it)")

    def errConnectionLost(self):
        log.err("errConnectionLost! The child closed their stderr.")

    def processExited(self, reason):
        log.msg("Minecraft process exited, code %d" % reason.value.exitCode)

    def processEnded(self, reason):
        log.msg("Stopping reactor.")
        reactor.stop()

    def cmd_list_players(self):
        """
        Pipes in a 'list' command to the interactive Minecraft server PTY.
        Returns the result via a deferred.

        :rtype: defer.Deferred
        :returns: a Deferred object to add a callback that will receive
            a string value containing the connected players list.
        """
        deferred = defer.Deferred()
        # Toss a deferred on the end of the stack, since we're FIFO.
        self._player_list_deferreds.append(deferred)
        
        # Pipe the 'list' command into the Minecraft server's stdin.
        self.send_mc_command('list')

        # Get the deferred we just appended.
        return deferred

    def _parse_lines(self, data):
        """
        Splits a raw string into a list of separate lines.

        :rtype: list
        :returns: Each individual line that was passed in the globby string.
        """
        return data.strip().split('\r\n')

    def outReceived(self, bytes):
        """
        stdout just got some data. Determine what it is, see if it's
        interesting to us, and pass it along accordingly.

        :param str bytes: The data received from stdout.
        """
        outbuffer = self.outbuffer + bytes
        print bytes
        #lines, leftover = self.parseLines(outbuffer)
        lines = self._parse_lines(outbuffer)
        #self.outbuffer = leftover

        for line in lines:
            # We're only interested in Connected players output for now.
            if 'Connected players:' not in line:
                continue

            # On almost every message, first four characters are the year.
            year = line[:4]
            # This is a silly/lazy way of seeing if this is interesting
            # output, without having to write a real parser.
            # TODO: Write a real stdout parser.
            if str(datetime.date.today().year) != year:
                continue

            self._parse_connected_players_output(line)

    def _parse_connected_players_output(self, line):
        """
        Since we have already identified ``line`` as a Connected players line,
        this method parses it and returns the callback for the web API.
        """
        # Get the text after the year/timestamp.
        line_nodate = line[19:].strip()
        if line_nodate.startswith('['):
            # This probably has a tag, like [INFO]. Almost everything
            # does, so this is where most things fall.
            split = line_nodate.split()
            # [INFO]
            tag = split[0]
            # The meat of the output message.
            output = ' '.join(split[1:])
        else:
            # There's no [INFO] or other tag, leave this be.
            tag = None
            output = line_nodate

        # Watch for some key strings that that only happen when a sever
        # command is piped into stdin.
        if output.startswith('Connected players:'):
            # Found the output of the 'list' command. This happened as
            # a result of web_api.resources.CmdListConnected being hit.

            # Get the text after 'Connected players:'.
            player_str = output[18:]
            if not player_str:
                # No players connected.
                players = []
            else:
                # Players found. Make a player list to return.
                players = player_str.replace(' ', '').split(',')

            # Need to get the first deferred from the pending stack,
            # since that is the oldest outstanding request.
            self._player_list_deferreds.pop(0).callback(players)

    def send_mc_command(self, command_str):
        """
        Convenience method for sending a command

        :param str command_str: The command to send to the Minecraft server,
            without \n or \r sequences on the end.
        """
        self.transport.write("%s\n" % command_str)