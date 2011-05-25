zombiepygman
============

zombiepygman is a Minecraft_ server wrapper written in Python_. While there
are no lack for server wrappers, this project is notable for a few reasons:

* The Minecraft server may be controlled via a JSON API.
* For commands that return output (list), unlike many wrappers, you can
  actually get the command's output via the API as well. So it becomes
  possible to display your list of currently connected players without any
  Minecraft server mods.

.. _Minecraft: http://minecraft.net
.. _Python: http://python.org

Status
------

zombiepygman is early on in development, but already very much usable.
Documentation is completely absent, and things are likely to change without
notice. Packaging is completely absent.

Things will continue to shape up as long as this project remains interesting
to me. Feel free to fork/pull request!

Requirements
------------

* Python 2.6+
* Twisted 11.0+
* simplejson

Installation
------------

This is currently a little rough, but this will get you running.

* Download or ``git clone`` the repository. Extract it where you'd like to
  run your Minecraft server from.
* Download minecraft_server.jar, toss it in the root level zombiepygman
  directory (not ``zombiepygman/zombiepygman``).
* Run ``java -jar minecraft_server.jar`` once to get all of the config
  and support files created. Stop the server.
* Start zombiepygman: ``twistd -ny server.tac``. If you want to run in
  daemon mode, omit the 'n': ``twistd -y server.tac``.
* Your JSON API is available on port 8000 by default.

Support
-------

Direct all questions, bugs, ideas, and suggestions to the `issue tracker`_.

.. _issue tracker: https://github.com/gtaylor/zombiepygman/issues

License
-------

zombiepygman is licensed under the `BSD License`_.

.. _BSD License: https://github.com/gtaylor/zombiepygman/blob/master/LICENSE
