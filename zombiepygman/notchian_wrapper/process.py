"""
The :class:`NotchianProcess` class handles some process management tasks.

Signal handlers intercept the default SIGQUIT, SIGINT, and SIGTERM behaviors,
and instead send commands through the Minecraft server that eventually
cascade into reactor.stop().
"""
import os
import signal
from twisted.internet import reactor
from twisted.python import log
from zombiepygman.notchian_wrapper.protocol import NotchianProcessProtocol
from zombiepygman.conf import settings

class NotchianProcess(object):
    """
    This object wraps the minecraft_server.jar's process. All communication
    with the
    """
    # The NotchianProcessProtocol class, which is how you send/receive data
    # from minecraft_server.jar's server process.
    protocol = None

    @classmethod
    def start_minecraft_server(cls):
        """
        Handles starting the Minecraft process and populating the
        cls.protocol attribute.
        """
        process_name = "zombiepygman"
        startup_args = [settings.PROCESS_NAME]
        startup_args += settings.JAVA_FLAGS + ['-jar']
        startup_args += [settings.MINECRAFT_SERVER_JAR_PATH] + ['nogui']
        
        cls.protocol = NotchianProcessProtocol()
        start_command_str = ' '.join(startup_args[1:])
        log.msg('Starting Minecraft with: java %s' % start_command_str)
        reactor.spawnProcess(
            cls.protocol,
            settings.JAVA_BIN_PATH,
            args=startup_args,
            env={},
            path=settings.MINECRAFT_SERVER_DATA_DIR,
            usePTY=True,
        )

    @classmethod
    def stop_minecraft_server(cls, wait_secs=None):
        """
        Announces impending shutdown, then stops the Minecraft server process,
        consequently bringing the zombiepygman daemon down too.

        :keyword int wait_secs: The number of seconds to wait after
            announcing the server shutdown until actually shutting down.
            It's polite to give players a heads up, since a shutdown can be
            mistaken for connection issues due to the undescriptive error
            messages on the client.
        """
        wait_secs = settings.DEFAULT_SHUTDOWN_DELAY or wait_secs
        announcement = 'say Server is going down in %d seconds.' % wait_secs
        cls.protocol.send_mc_command(announcement)
        # After however long a wait specified, issue the shutdown command.
        reactor.callLater(wait_secs, cls.protocol.send_mc_command, 'stop')

    @classmethod
    def _stop_gracefully_signal_handler(cls, sig_number, stack_frame):
        """
        Signal handler for any signal that asks for a graceful stoppage of
        the Minecraft server. Allows time for announcing the shutdown,
        saving the world, and letting everything wrap up.
        """
        try:
            cls.stop_minecraft_server()
        except AttributeError:
            # The server didn't fully start, we'll have to just manually
            # stop the reactor here.
            log.err("Server didn't fully start. Stopping the reactor "\
                    "manually.")
            reactor.stop()

"""
Signal handling

We can't just use Twisted's reactor events, since the reactor can stop before
the Minecraft process is done shutting down. By capturing the signals here,
we can send a 'stop' command to the Minecraft server, causing the
NotchianProcessProtocol.processEnded callback to be fired, which calls
reactor.stop().
"""
signal_handler = NotchianProcess._stop_gracefully_signal_handler
# Clean termination.
signal.signal(signal.SIGTERM, signal_handler)
# Interrupt character.
signal.signal(signal.SIGINT, signal_handler)
# Another interrupt character.
signal.signal(signal.SIGQUIT, signal_handler)
