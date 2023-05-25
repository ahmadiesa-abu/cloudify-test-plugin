from pyVim.connect import SmartConnect, Disconnect
from . import vapi_connect


class ServiceManager(object):
    """
    Manages Vim and vAPI services on a management node.
    """
    def __init__(self, server, username, password, skip_verification):

        self.server_url = server
        self.username = username
        self.password = password
        self.skip_verification = skip_verification
        self.vapi_url = None
        self.vim_url = None
        self.session = None
        self.session_id = None
        self.stub_config = None
        self.si = None
        self.content = None
        self.vim_uuid = None

    def connect(self):
        # Connect to vAPI Endpoint on vCenter Server system
        self.stub_config = vapi_connect.connect(host=self.server_url,
                                               user=self.username,
                                               pwd=self.password,
                                               skip_verification=self.skip_verification)

        # Connect to VIM API Endpoint on vCenter Server system
        context = None
        if self.skip_verification:
            context = vapi_connect.get_unverified_context()
        self.si = SmartConnect(host=self.server_url,
                               user=self.username,
                               pwd=self.password,
                               sslContext=context)
        assert self.si is not None

        # Retrieve the service content
        self.content = self.si.RetrieveContent()
        assert self.content is not None
        self.vim_uuid = self.content.about.instanceUuid

    def disconnect(self):
        vapi_connect.logout(self.stub_config)
        Disconnect(self.si)