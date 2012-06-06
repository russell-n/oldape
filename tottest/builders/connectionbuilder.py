"""
A module to build the dut connection
"""

from tottest.connections import adbconnection
from tottest.baseclass import BaseClass


class DutConnection(BaseClass):
    """
    """
    def __init__(self, parameters=None):
        super(DutConnection, self).__init__()
        self._connection = None
        return

    @property
    def connection(self):
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection
    

