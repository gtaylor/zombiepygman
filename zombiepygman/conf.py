"""
zombiepygman-specific configuration classes, utilities, and global 'settings'
instance.

If you're writing something that needs settings, you'll want to do something
like this::

    from zombiepygman.conf import settings
    val = settings.SOME_SETTING
"""
import os
import config

class SettingsStore(object):
    """
    The sole purpose of this object is to grab user-specified values from
    conf.py in the root of the project, or abstract the use of defaults in the
    absence of overrides.
    """
    def __init__(self):
        # The path to the root of the zombiepygman install. This will be the
        # directory that contains config.py by default.
        self._calc_conf('ROOT_DIR', self.__get_default_root_dir())
        # The port to run the JSON API on.
        self._calc_conf('API_PORT', 8000)
        # The delay (in seconds) to from the time the 'stop' JSON API call is
        # made, to the point where the server is actually shut down. An
        # announcement is made via 'say' to let the players know things are
        # going down. This can be 0, but it's more informative if the players
        # know why their client suddenly errored out.
        self._calc_conf('DEFAULT_SHUTDOWN_DELAY', 1.0)
        # This is a really really low-fi attempt at at least not hanging the
        # API's ass out the window. If this is a None value at start time,
        # zombiepygman will terminate and nag the user.
        self._calc_conf('API_SECURITY_TOKEN', None)
        # The path to your java binary.
        self._calc_conf('JAVA_BIN_PATH', 'java')
        # Flags to use with the 'java' command during startup. For example,
        # ['-Xmx1024M', '-Xms1024M']
        self._calc_conf('JAVA_FLAGS', ['-Xmx1024M', '-Xms1024M'])
        # The path to your minecraft_server.jar achive.
        self._calc_conf('MINECRAFT_SERVER_JAR_PATH',
            os.path.join(
                self.ROOT_DIR,
                'minecraft_server',
                'minecraft_server.jar'
            )
        )
        # For OSs and distro configurations that support it, this re-names
        # the process. Might require admin/root in most cases.
        self._calc_conf('PROCESS_NAME', 'zombiepygman')
        # This is the server's data dir, where the server config, whitelist,
        # and world dir is kept.
        self._calc_conf('MINECRAFT_SERVER_DATA_DIR',
                        self.__get_default_minecraft_server_data_dir())

    def __get_default_root_dir(self):
        """
        Returns the default zombiepygman root dir, if none is specified.
        Defaults to the same location that the config.py file is in.

        :rtype: str
        :returns: The root directory path.
        """
        return os.path.dirname(os.path.abspath(config.__file__))

    def __get_default_minecraft_server_data_dir(self):
        """
        Returns the path to the directory to stash all of the files that
         minecraft_server.jar creates/maintains in.

        :rtype: str
        :returns: Path to the Minecraft server's data dir.
        """
        return os.path.join(self.ROOT_DIR, 'minecraft_server')

    def _calc_conf(self, setting, default_val):
        """
        Abstracts the settings retrieval from the source of custom settings.
        Sets the setting on the :class:`SettingsStore` object as an attribute.

        :param str setting: The setting to get/set the value for.
        :param instance default_val: The default value for the setting,
            if no match can be found in the user's config.
        """
        setattr(self, setting, getattr(config, setting, default_val))

# Settings values can be accessed by importing this into your modules.
settings = SettingsStore()