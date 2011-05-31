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
    def __init__(self):
        # Timeout API requests after this many seconds.
        self.SOCKET_TIMEOUT = 5
        # The full URI to the zombiepygman's TCP server. No trailing slash.
        self.API_HOST = 'http://localhost:8001'
        # Your API security token. This must match what you have configured
        # in zombiepygman's conf.py.
        self.SECURITY_TOKEN = None

    def _call_zpg_api(self, path, **kwargs):
        """
        Make an API call to the zombiepygman instance configured in the site's
        settings.
    
        Any keyword args provided become GET NVPs for the API request.

        :rtype: dict
        :returns: The un-serialized API response in dict form.
        """
        # Beware, this is a global setting.
        socket.setdefaulttimeout(self.SOCKET_TIMEOUT)

        logger.debug('ZPG API host: %s' % self.API_HOST)

        # This will store key/value pairs to be used as GET NVPs in the request.
        http_get_vals = {
            'security_token': self.SECURITY_TOKEN
        }
        # All values passed to PayPal API must be uppercase.
        for key, value in kwargs.iteritems():
            http_get_vals[key.upper()] = value

        # This shows all of the key/val pairs we're sending to PayPal.
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug('ZPG API Query Key/Vals:\n%s' % pformat(http_get_vals))

        # Turn kwargs into GET NVPs.
        data = urllib.urlencode(http_get_vals)
        if data:
            data = '?%s' % data

        # Full Proto + Host + URL Path + GET NVPs for API Resource.
        full_url = '%s%s%s' % (self.API_HOST, path, data)
        logging.debug('ZPG API Query URL: %s' % full_url)

        # Do work, son.
        req = urllib2.Request(full_url)
        response = urllib2.urlopen(req).read()
        response_dict = json.loads(response)

        logging.debug('ZPG API Response:\n%s' % pformat(response_dict))
        return response_dict
