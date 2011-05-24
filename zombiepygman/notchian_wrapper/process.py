from twisted.internet import reactor
from zombiepygman.notchian_wrapper.protocol import NotchianProcessProtocol

# This will contain the transport instance, used for writing to/from
# the Minecraft process.
transport = None

def start_minecraft_server():
    """
    Handles starting the Minecraft process and populating the module's transport
    variable.
    """
    global transport

    # TODO: Set these via configs.
    java_bin = "java"
    process_name = "minecraft"

    transport = reactor.spawnProcess(
        NotchianProcessProtocol(),
        java_bin,
            [
                process_name,
                "-jar",
                "minecraft_server.jar",
                "nogui"
            ], {}
    )