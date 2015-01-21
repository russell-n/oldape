
#from apetools.commands.ifconfig import IfconfigCommand
#from apetools.commands.iwconfig import Iwconfig
from apetools.commons.enumerations import OperatingSystem
from apetools.devices.basedevice import BaseDevice
from apetools.commons.errors import ConfigurationError


class IosDevice(BaseDevice):
    """
    A class to query ios devices (pretty much nothing is implemented on the ipad).

     * this is mostly a dummy to hold settings
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `connection`: a connection to the device
         - `interface`: the name of the test interface (to get the ip address)
        """
        super(IosDevice, self).__init__(*args, **kwargs)
        return

    @property
    def address(self):
        """
        :return: the address of the device
        :raise: ConfigurationError if not set by user
        """
        if self._address is None:
            raise ConfigurationError("'test_address' must be set in config for IOS devices")
        return self._address

    @property
    def mac_address(self):
        """
        Not implemented
        
        :return: the MAC address of the device
        """
        self.logger.warning('mac address query not implemented')
        return 'NA'

    @property
    def bssid(self):
        """
        Not implemented
        """
        self.logger.warning('bssid query not implemented')
        return 'NA'
    
    @property
    def ssid(self):
        """
        Not implemented
        """
        self.logger.warning('ssid query not implemented')
        return 'NA'

    @property
    def noise(self):
        """
        Not Implemented
        """
        self.logger.warning('noise query not implemented')
        return 'NA'

    @property
    def channel(self):
        """
        Not implemented
        """
        self.logger.warning('channel not implemented')
        return "NA"
    
    @property
    def rssi(self):
        """
        Not implemented
        
        :return: rssi from the wifi_query
        """
        self.logger.warning('rssi query not implemented')
        return "NA"

    @property
    def bitrate(self):
        """
        Not implemented
        
        :return: NA
        """
        self.logger.warning("bitrate query not implemented")
        return "NA"

    def disable_wifi(self):
        """
        Not implemented
        """
        self.logger.warning('disable wifi not implemented')
        return

    def enable_wifi(self):
        """
        Not implemented
        """
        self.logger.warning('enable wifi not implemented')
        return

    def log(self, message):
        """
        Sends the message to the syslog (Not implemented)
        
        :param:

         - `message`: a string to send to the syslog

        :postcondition: message sent to the syslog
        """
        # This uses the call interface because the connection has its own logger property 
        self.logger.warning('log not implemented')
        return
# end IosDevice
