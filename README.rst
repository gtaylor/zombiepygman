zombiepygman
============

zombiepygman is a Minecraft_ server wrapper written in Python_. While there
are no lack for server wrappers, this project is notable for a few reasons:

* The Minecraft server may be controlled via a JSON API.
* For commands that return output (list), unlike many wrappers, you can
  actually get the command's output via the API as well. So it becomes
  possible to display your list of currently connected players without any
  Minecraft server mods.
* You may query the API to retrieve various bits of world-related data, like
  the coordinates of individual or all players.
* A lot of functionality can be scripted/scheduled, instead of using
  bukkit plugins.

.. _Minecraft: http://minecraft.net
.. _Python: http://python.org

Status
------

zombiepygman is early on in development, but already very much usable.
Documentation is completely absent, and things are likely to change without
notice.

Things will continue to shape up as long as this project remains interesting
to me. Feel free to fork/pull request!

Requirements
------------

* Python 2.6 or 2.7 (may work on earlier versions, but is un-tested)
* Twisted 11.0+ (may work on earlier versions, but is un-tested)
* simplejson
* Only tested on Mac/Linux, but should theoretically work on Windows

Installation
------------

This is currently a little rough, but this will get you running.

* Install requirements: ``pip install -r requirements.txt``
* If you don't have pip: ``easy_install twisted simplejson``
* Download or ``git clone`` the repository. Extract it where you'd like to
  run your Minecraft server from.
* Download minecraft_server.jar, toss it in the root level
  minecraft_server directory.
* Copy ``config_example.py`` to ``config.py`` in your root zombiepygman
  directory. Edit the value for ``API_SECURITY_TOKEN`` at the very least.
* Take a minute to set up firewall rules to prevent outside access to
  zombiepygman. If the API will be consumed on the same machine, we recommend
  only allowing access via loopback on your API port (8001 by default). Failing
  to do this is just asking for someone to do mean things to you.

Starting zombiepygman
---------------------

* Start zombiepygman: ``twistd -ny server.tac``. If you want to run in
  daemon mode, omit the 'n': ``twistd -y server.tac``.
* Your JSON API is available on port 8001 by default.

Basic API client
----------------

You'll find a really basic example API client in zombiepygman.client. Here
is an example of how to use it::

    from zombiepygman.client import ZpmAPI

    # This has to match on both client and server.
    token = 'YOUR_TOKEN_HERE'
    api = ZpmAPI(security_token=token)

    # An example instance of piping commands into the server console and
    # retrieving the output. All API calls return dicts from JSON.
    results = api.cmd_list_connected()
    # A list of connected players, or an empty list if none.
    players = results['player_list']

    # Querying for player locations for specific players. Omit the kwarg
    # to return locations for all known players who have ever logged in
    # to your server.
    results = api.get_playerlocs(for_players=['SomeBromo', 'SomeBraski'])
    locs = results['player_locs']
    my_loc = locs['SomeBromo']


Running Unit Tests
------------------

For developers, you may run the unit tests by doing the following::

    pip install nose
    # From within your root zombiepygman dir:
    nosetests

Support
-------

Direct all questions, bugs, ideas, and suggestions to the `issue tracker`_.

.. _issue tracker: https://github.com/gtaylor/zombiepygman/issues

License
-------

zombiepygman is licensed under the `BSD License`_.

.. _BSD License: https://github.com/gtaylor/zombiepygman/blob/master/LICENSE
