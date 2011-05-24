"""
This module assembles the various API sub-modules into URL paths. These become
the JSON API that external software can POST to for various things.
"""
import cgi
from txrestapi.resource import APIResource
from zombiepygman.web_api.views import JobSubmitView

"""
URL assembly.
"""
API = APIResource()

API.register('POST', '^/job/submit', JobSubmitView)
