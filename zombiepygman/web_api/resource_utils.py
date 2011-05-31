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

        # This holds the user's parsed JSON input, if applicable.
        self.user_input = None
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

    def parse_user_input(self, request):
        """
        Parses the user's JSON input.

        :returns: The user's input dict, or None if there was no input.
        """
        request.content.seek(0)
        raw_input = request.content.read()

        if raw_input:
            full_dict = simplejson.loads(raw_input)
            self.user_input = full_dict.get('payload', None)
        return self.user_input

    def get_context(self, request):
        """
        Adjusts the :attr:`context` attribute to contain whatever data will
        be returned by :meth:`render_POST`.
        """
        pass

    def get_context_json(self):
        """
        Handle construction of the response and return it.

        :rtype: str
        :returns: A serialized JSON string to return to the user.
        """
        return simplejson.dumps(self.context)

    def render_POST(self, request):
        """
        Finishes up the rendering by returning the JSON dump of the context.

        :rtype: str
        :returns: The JSON-serialized context dict.
        """
        self.parse_user_input(request)
        self.get_context(request)
        return self.get_context_json()

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

        # The get POST data (a JSON string).
        request.content.seek(0)
        content = request.content.read()
        # Parse the JSON string.
        data = simplejson.loads(content)
        # Compare provided security token to token in conf.py.
        return str(settings.API_SECURITY_TOKEN) == data['security_token']

class PermissionDeniedResource(JSONResourceMixin):
    """
    Return this Resource when an invalid security token is found.
    """
    def render_POST(self, request):
        self.set_error('Invalid API security token.')
        return self.get_context_json()
