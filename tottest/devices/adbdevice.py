"""
An ADB Device
"""

from basedevice import BaseDevice
from tottest.connections import adbconnection

class AdbDevice(BaseDevice):
    def __init__(self, connection=None, wifi_tool=None, interface=None, *args, **kwargs):
        """
        :param:

         - `connection`: An adb device connection
         - `wifi_command`: The wifi command to get 
        """
        self._connection = connection
        self._logger = None
        self._wifi_tool = wifi_tool
        self._interface = interface
        return

    @property
    def connection(self):
        """
        :return: A connection to the device. 
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection

    @property
    def wifi_tool(self):
        """
        """
        return 


    def wake_screen(self):
        """
        Acquire the wake lock.
        """
        raise NotImplementedError("AdbDevice.wake_screen not implemented")
        return

    
    def display(self, message):
        """
        Display an image on the screen
        """
        raise NotImplementedError("AdbDevice.display not implemented")
        return

    
    def disable_wifi(self):
        """
        Disable the WiFi Radio
        """
        raise NotImplementedError("AdbDevice.disable_wifi not implemented (yet)")
        return

    
    def enable_wifi(self):
        """
        Enable the WiFi radio.
        """
        raise NotImplementedError("AdbDevice.enable_wifi not implemented (yet).")
        return
    
    
    def get_wifi_info(self):
        """
        :rtype: StringType
        :return: The Wifi Info
        """
        raise NotImplementedError("AdbDevice.get_wifi_info not implemented (yet).")
        return
    
    
    def log(self, message):
        """
        Send a message to the device's log.

        :param:

         - `message`: A string to send to the device log.
        """
        self.connection.log(message)
        return
# end class AdbDevice
