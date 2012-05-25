"""
The Abstract Base for devices
"""
# python
from abc import ABCMeta, abstractproperty, abstractmethod

#local
from timetorecovertest.baseclass import BaseClass


class BaseDevice(BaseClass):
    __metaclass__ = ABCMeta
    def __init__(self, connection=None, *args, **kwargs):
        """
        :param:

         - `connection`: An device connection
        """
        self._connection = connection
        self._logger = None
        return

    @abstractproperty
    def connection(self):
        """
        :return: A connection to the device. 
        """
        if self._connection is None:
            self._connection = None
        return self._connection

    @abstractmethod
    def wake_screen(self):
        """
        Acquire the wake lock.
        """
        return

    @abstractmethod
    def display(self, message):
        """
        Display an image on the screen
        """
        return

    @abstractmethod
    def disable_wifi(self):
        """
        Disable the WiFi Radio
        """
        return

    @abstractmethod
    def enable_wifi(self):
        """
        Enable the WiFi radio.
        """
        return
    
    @abstractmethod
    def get_wifi_info(self):
        """
        :rtype: StringType
        :return: The Wifi Info
        """
        return
    
    @abstractmethod
    def log(self, message):
        """
        Send a message to the device's log.

        :param:

         - `message`: A string to send to the device log.
        """
        return
# end class BaseDevice
