"""
An ADB device
"""

from basedevice import BaseDevice
from tottest.connections.adbconnection import ADBShellConnection
from tottest.commands.svc import Svc

class AdbDevice(BaseDevice):
    """
    A class to bundle commands to control an adb device
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
        """
        super(AdbDevice, self).__init__(*args, **kwargs)
        self._wifi_control = None
        return

    @property
    def wifi_control(self):
        """
        """
        if self._wifi_control is None:
            self._wifi_control = Svc(connection=self.connection)
        return self._wifi_control

    @property
    def connection(self):
        """
        :return: connection passed in or ADBShellConnection if not given
        """
        if self._connection is None:
            self._connection = ADBShellConnection()
        return self._connection

    def wake_screen(self):
        """
        Wake the screen
        """
        raise NotImplementedError("Wake Screen not ready yet")
        return

    def display(self, message):
        """
        Display a message on the screen
        """
        raise NotImplementedError("Display <message> not done yet")
        return

    def disable_wifi(self):
        """
        :postcondition: WiFi radio disabled
        """
        self.wifi_control.disable_wifi()
        return

    def enable_wifi(self):
        """
        :postcondition: WiFi radio enabled
        """
        self.wifi_control.enable_wifi()
        return

    def get_wifi_info(self):
        """
        :rtype: StringType
        :return: The Wifi Info
        """
        raise NotImplementedError("Get WiFi Info not done yet")
        return

    def log(self, message):
        """
        :postcondition: message sent to the connection
        """
        self.connection.log(message)
        return

    def root(self):
        """
        :postcondition: `su` sent to the device
        """
        self.connection.su(timeout=1)
        return
# end class AdbDevice
