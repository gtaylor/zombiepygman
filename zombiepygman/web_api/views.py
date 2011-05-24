import cgi
import simplejson
from zombiepygman.web_api.base_views import BaseView
from zombiepygman.notchian_wrapper.process import NotchianProcess

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

class CmdListView(BaseView):
    """
    Retrieves a list of connected players.
    """
    def view(self):
        NotchianProcess.transport.writeSomeData('list')
        #self.context.update({})