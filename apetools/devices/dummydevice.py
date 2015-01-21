
from apetools.baseclass import BaseClass
from apetools.connections.localconnection import OutputError


class DummyConnection(BaseClass):
    """
    A class to act as a fake connection.
    """
    def __init__(self):
        super(DummyConnection, self).__init__()
        return

    def _procedure_call(self, command, arguments, timeout):
        """
        Logs the command and arguments then returns empty strings

        :param:

         - `command`: command to send to the connection
         - `arguments`: arguments for the command
         - `timeout`: readline timeout

        :return: OutputError with empty strings as data
        """
        self.logger.info("DummyCall: {0} {1}".format(command, arguments))
        return OutputError("", "")
    
    def __getattr__(self, command):
        """
        Calls _procedure call (enables the dot-notation calls)
        """
        def procedure_call(*args, **kwargs):
            return self._procedure_call(command, *args, **kwargs)
        return procedure_call
# end class DummyConnection


class DummyDevice(BaseClass):
    """
    A class to configure and query linux devices
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

        """
        super(DummyDevice, self).__init__(*args, **kwargs)
        self._connection = None
        return

    @property
    def connection(self):
        """
        :return: a Dummy Connection
        """
        if self._connection is None:
            self._connection = DummyConnection()
        return self._connection
        
    @property
    def address(self):
        """
        :return: the address of the device
        """
        return "DummyAddress"

    @property
    def mac_address(self):
        """
        :return: the MAC address of the device
        """
        return "DummyMac"

    @property
    def bssid(self):
        """
        Fake Basic service set identification 
        """
        return "DummyBSSID"
    
    @property
    def wifi_info(self):
        """
        :return: a summary string of available wifi info.
        """
        return "SSID:\t{ssid}\nBSSID:\t{bssid}\nRSSI:\t{rssi}\nIP Address:\t{ip}\nMAC:\t{mac}\n".format(ssid=self.ssid,
                                                                                                        bssid=self.bssid,
                                                                                                        rssi=self.rssi,
                                                                                                        ip=self.address,
                                                                                                        mac=self.mac_address)

    @property
    def ssid(self):
        """
        Fake identifier for the AP
        """
        return "DummySSID"
    
    @property
    def rssi(self):
        """
        :return: rssi from the wifi_query
        """
        return "DummyRSSI"
    
    def disable_wifi(self):
        """
        Logs the fact that this method was called.
        """
        self.logger.info("Disable WiFi Called")
        return

    def enable_wifi(self):
        """
        Logs the fact that this method was called
        """
        self.logger.info("Enable WiFi Called")
        return

    def log(self, message):
        """
        :param:

         - `message`: a string to send to the syslog

        :postcondition: message sent to the syslog
        """
        self.logger.info(message)
        return
# end class DummyDevice
