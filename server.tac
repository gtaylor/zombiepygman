"""
Start your Minecraft server from here, something like so::

    twistd -y server.tac

If you want interactive (non-daemon) mode::

    twistd -ny server.tac
"""
from zombiepygman.server import application