
from apetools.commands import dumpsyswifi
from apetools.commands import netcfg
from apetools.connections import adbconnection


class TestDumpsysWifi(object):
    """
    Gathers wifi information for a sanity check.
    """
    def __init__(self, parameters):
        """
        :param:

         - `parameters`: object with the wifi_interface attribute
        """
        self.parameters = parameters
        self._dumpsys = None
        self._connection = None
        self._netcfg = None
        return

    @property
    def connection(self):
        """
        :return: ADBShellConnection
        """
        if self._connection is None:
            self._connection = adbconnection.ADBShellConnection()
        return self._connection

    @property
    def dumpsys(self):
        """
        :return: DumpsysWifi object
        """
        if self._dumpsys is None:
            self._dumpsys = dumpsyswifi.DumpsysWifi()
        return self._dumpsys

    @property
    def netcfg(self):
        """
        :return: NetcfgCommand
        """
        if self._netcfg is None:
            self._netcfg = netcfg.NetcfgCommand(self.connection,
                                                self.parameters.wifi_interface)
        return self._netcfg

    def __call__(self):
        """
        :postcondition: DumpsysWifi info and IP Address Displayed on screen
        """
        print "*" * 40
        print str(self.dumpsys)
        print self.netcfg.ip_address
        print "*" * 40
        return
