from twisted.internet import reactor
from zombiepygman.notchian_wrapper.protocol import NotchianProcessProtocol

class NotchianProcess(object):
    # IProcessTransport instance.
    transport = None
    protocol = None

    @classmethod
    def start_minecraft_server(cls):
        """
        Handles starting the Minecraft process and populating the module's transport
        variable.
        """
        # TODO: Set these via configs.
        java_bin = "java"
        process_name = "minecraft"
        cls.protocol = NotchianProcessProtocol()

        cls.transport = reactor.spawnProcess(
            cls.protocol,
            java_bin,
            args=[
                process_name,
                "-jar",
                "minecraft_server.jar",
                "nogui"
            ],
            env={},
            usePTY=True,
        )