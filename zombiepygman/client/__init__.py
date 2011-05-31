"""
A very simple sync API client. You can roll your own as needed if this
does not meet your needs.

You'll want to import ZpmAPI, and instantiate/use it like this::

    api = ZpmAPI()
    results = api.cmd_list_connected()
    print("RESULTS")
    print(results)
"""
from zombiepygman.client.api import ZpmAPI