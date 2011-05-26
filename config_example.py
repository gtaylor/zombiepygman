"""
Example config.py file. You'll want to copy this to config.py and edit
the default values before trying to start zombiepygman.

To see the full list of possible values and their defaults, refer
to SettingsStore in::

    https://github.com/gtaylor/zombiepygman/blob/master/zombiepygman/conf.py
"""

# The port to run the JSON API on.
API_PORT = 8001

# This is a really really low-fi attempt at at least not hanging the
# API's ass out the window. If this is a None value at start time,
# zombiepygman will terminate and nag the user.
# NOTE: You have to set this to some string value before zombiepygman will
# cooperate with you.
API_SECURITY_TOKEN = None

# The path to your java binary.
JAVA_BIN_PATH = 'java'

# Flags to use with the 'java' command during startup. For example,
# ['-Xmx1024M', '-Xms1024M']
JAVA_FLAGS = ['-Xmx1024M', '-Xms1024M']
