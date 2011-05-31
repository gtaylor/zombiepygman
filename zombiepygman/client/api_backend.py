"""
Boring backend stuff. This can be replaced with less boring stuff if you
so desire.
"""
import socket
import logging
import urllib
import urllib2
from pprint import pformat
import json

logger = logging.getLogger('zombiepygman.client.api_backend')

class APIBackend(object):
    """
    Backend class that handles stuff like HTTP transport, configuration,
    and etc.
    """
    def __init__(self, socket_timeout=5, api_host='http://localhost:8001',
                 security_token=None):
        # Timeout API requests after this many seconds.
        self.SOCKET_TIMEOUT = socket_timeout
        # The full URI to the zombiepygman's TCP server. No trailing slash.
        self.API_HOST = api_host
        # Your API security token. This must match what you have configured
        # in zombiepygman's conf.py.
        self.SECURITY_TOKEN = security_token

    def _call_zpg_api(self, path, payload=None):
        """
        Make an API call to the zombiepygman instance configured in the site's
        settings.
    
        Any keyword args provided become GET NVPs for the API request.

        :param dict payload: The payload to attach to this API request. Should
            be a dict, and may contain any other JSON-serializable type.
        :rtype: dict
        :returns: The un-serialized API response in dict form.
        """
        # Beware, this is a global setting.
        socket.setdefaulttimeout(self.SOCKET_TIMEOUT)

        logger.debug('ZPG API host: %s' % self.API_HOST)

        if not payload:
            payload = {}

        # This is the top-level dict that gets sent to zpm.
        data = {
            'security_token': self.SECURITY_TOKEN,
            'payload': payload,
        }

        # This shows all of the key/val pairs we're sending to PayPal.
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('ZPG API Query Key/Vals:\n%s' % pformat(data))

        # Full Proto + Host + URL Path + GET NVPs for API Resource.
        full_url = '%s%s' % (self.API_HOST, path)
        logging.debug('ZPG API Query URL: %s' % full_url)

        # Do work, son.
        req = urllib2.Request(full_url, json.dumps(data))
        response = urllib2.urlopen(req).read()
        response_dict = json.loads(response)

        logging.debug('ZPG API Response:\n%s' % pformat(response_dict))
        return response_dict
