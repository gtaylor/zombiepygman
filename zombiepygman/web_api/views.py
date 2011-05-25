import cgi
import simplejson
from zombiepygman.web_api.base_views import BaseView
from zombiepygman.notchian_wrapper.process import NotchianProcess
from zombiepygman.notchian_wrapper.unsafe_store import PlayerListStore

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
    def _callback(self, data):
        print "CALLBACK", data
        self.context.update({'players': data})
        return data

    def view(self):
        dfunc = NotchianProcess.protocol.listPlayers()
        dfunc.addCallback(self._callback)
        self.context.update({'testVal': None})