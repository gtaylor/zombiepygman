"""
Some assorted parent classes, mixins, and helper functions for resources.
"""
import simplejson
from twisted.web.resource import Resource

class JSONResourceMixin(Resource):
    """
    Mixin for JSON Resource objects. No particular execution order is
    enforced here, just return the value of :method:`get_context_json` to
    the user.
    """
    def __init__(self, *args, **kwargs):
        """
        Important part to note here is that self.context is the dict that
        we serialize and return to the user. Add any key/values in here that
        the user needs to see.
        """
        Resource.__init__(self)

        # The payload we return to the user.
        self.context = {
            'success': True
        }

    def set_error(self, message):
        """
        Sets an error state and HTTP code.

        :param str message: The error message to return in the response.
        """
        self.context = {
            'success': False,
            'message': message,
        }

    def get_context_json(self):
        """
        Handle construction of the response and return it.

        :rtype: str
        :returns: A serialized JSON string to return to the user.
        """
        return simplejson.dumps(self.context)
