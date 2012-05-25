"""
An SL4a Device provides the common device-methods using an SL4a connection
"""

from timetorecovertest.connections.sl4aconnection import SL4AConnection
from basedevice import BaseDevice


COMMA = ','
KEY_VALUE = "{k}:{v}"


class SL4ADevice(BaseDevice):
    def __init__(self, connection=None, *args, **kwargs):
        """
        :param:

         - `connection`: An SL4AConnection
        """
        self._connection = connection
        return

    @property
    def connection(self):
        """
        :return: An SL4AConnection 
        """
        if self._connection is None:
            self._connection = SL4AConnection()
        return self._connection

    def wake_screen(self):
        self.connection.wakeLockAcquireFull()
        self.connection.makeToast('wake Up')
        return

    def display(self, message):
        self.connection.makeToast(message)
        return

    def disable_wifi(self):
        self.connection.toggleWifiState(False)
        return

    def enable_wifi(self):
        self.connection.toggleWifiState(True)
        return

    def log(self, message):
        """
        Send the message to the logcat log.
        """
        self.connection.log(message)
        return

    def get_wifi_info(self):
        """
        :return: The wifi information as a single csv line
        """
        return COMMA.join((KEY_VALUE.format(k=key, v=value) for key, value in
                           self.connection.wifiGetConnectionInfo().items()))
# end class SL4ADevice
