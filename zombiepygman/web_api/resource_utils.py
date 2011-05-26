"""
Some assorted parent classes, mixins, and helper functions for resources.
"""
import simplejson
from twisted.web.resource import Resource
from zombiepygman.conf import settings

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

class AuthenticationMixin(Resource):
    """
    Use this mixin with routing Resources that have getChild() implemented
    to help check the security token's validity. Run
    :meth:`is_valid_security_token`, and if False, return
    :class:`PermissionDeniedResource` from within your routing resource.
    """
    def _is_valid_security_token(self, request):
        """
        Checks a request for the correct security token, which is a GET
        value passed during the API call. Compares to the value in settings.

        :rtype: bool
        :returns: True if the security token is valid, false if not.
        """
        if not settings.API_SECURITY_ENABLED:
            # Security disabled, everyone gets in.
            return True

        token = request.args.get('security_token', [''])
        return str(settings.API_SECURITY_TOKEN) == token[0]

class PermissionDeniedResource(JSONResourceMixin):
    """
    Return this Resource when an invalid security token is found.
    """
    def render_GET(self, request):
        self.set_error('Invalid API security token.')
        return self.get_context_json()
