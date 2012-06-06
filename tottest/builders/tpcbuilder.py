"""
A module to build Traffic PC Connections
"""

from tottest.baseclass import BaseClass
from tottest.connections import sshconnection


class TpcConnection(BaseClass):
    """
    """
    def __init__(self, hostname, username, password):
        super(TpcConnection, self).__init__()
        self.hostname = hostname
        self.username = username
        self.password = password
        self._connection = None
        return

    @property
    def connection(self):
        if self._connection is None:
            self._connection = sshconnection.SSHConnection(hostname=self.hostname,
                                                           username=self.username,
                                                           password=self.password)
        return self._connection
        
        
