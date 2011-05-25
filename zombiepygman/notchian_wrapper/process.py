"""
The :class:`NotchianProcess` class handles some process management tasks.

Signal handlers intercept the default SIGQUIT, SIGINT, and SIGTERM behaviors,
and instead send commands through the Minecraft server that eventually
cascade into reactor.stop().
"""
import os
import signal
from twisted.internet import reactor
from zombiepygman.notchian_wrapper.protocol import NotchianProcessProtocol

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
        # TODO: Set these via configs.
        java_bin = "java"
        process_name = "minecraft"
        cls.protocol = NotchianProcessProtocol()

        reactor.spawnProcess(
            cls.protocol,
            java_bin,
            args=[
                process_name,
                "-jar",
                "minecraft_server.jar",
                "nogui"
            ],
            env={},
            path=cls.determine_minecraft_server_dir(),
            usePTY=True,
        )

    @classmethod
    def determine_minecraft_server_dir(cls):
        """
        Returns the full path to the minecraft_server dir that contains
        minecraft_server.jar and its support files.

        ..todo:: Make this configurable?
        
        :rtype: str
        :returns: The path to the minecraft_server directory.
        """
        this_file_path = os.path.abspath(__file__)
        this_dir_path = os.path.dirname(this_file_path)
        package_path = os.path.dirname(this_dir_path)
        root_path = os.path.dirname(package_path)
        retval = os.path.join(root_path, 'minecraft_server')
        return retval

    @classmethod
    def stop_minecraft_server(cls, wait_secs=5):
        """
        Announces impending shutdown, then stops the Minecraft server process,
        consequently bringing the zombiepygman daemon down too.

        :keyword int wait_secs: The number of seconds to wait after
            announcing the server shutdown until actually shutting down.
            It's polite to give players a heads up, since a shutdown can be
            mistaken for connection issues due to the undescriptive error
            messages on the client.
        """
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
        cls.stop_minecraft_server()

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
