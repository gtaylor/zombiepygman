import cgi
import simplejson
from zombiepygman.web_api.base_views import BaseView

class JobSubmitView(BaseView):
    """
    A test view.
    """
    def view(self):
        print "REQ", self.request.args
        print "KW", self.kwargs
        print "CONT", self.context

        # This is serialized and returned to the user.
        self.context.update({'job_id': 'FWEE'})
