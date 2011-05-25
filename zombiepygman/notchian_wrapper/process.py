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
                "minecraft_server/minecraft_server.jar",
                "nogui"
            ],
            env={},
            usePTY=True,
        )