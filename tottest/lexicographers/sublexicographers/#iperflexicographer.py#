#python
from collections import namedtuple

from tottest.baseclass import BaseClass
from tottest.commons.enumerations import IperfDefaults
from tottest.lexicographers.config_options import ConfigOptions

iperf_client_parameters = 'window len parallel interval format time'.split()
iperf_server_parameters = 'window'

class IperfClientParameters(namedtuple("IperfClientParameters", iperf_client_parameters)):
    """
    lexicographer.IperfClientParameters is a named tuple of raw parameters 
    """
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}_{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end IperfClientParameters

class IperfServerParameters(namedtuple("IperfServerParameters", iperf_server_parameters)):
    __slots__ = ()
    def __str__(self):
        return ','.join(("{f}_{v}".format(f=f, v=getattr(self, f))
                         for f in self._fields))
# end IperfServerParameters


class IperfLexicographer(BaseClass):
    """
    An Iperf Lexicographer translates a configration map to named tuples
    """
    def __init__(self, parser):
        """
        :param:

         - `parser`: a pre-loaded Configration Map
        """
        super(IperfLexicographer, self).__init__()
        self.parser = parser
        self.section = ConfigOptions.iperf_section
        self._window = None
        self._length = None
        self._parallel = None
        self._interval = None
        self._format = None
        self._time = None
        self._client_parameters = None
        self._server_parameters = None
        return

    @property
    def window(self):
        """
        :rtype: String
        :return: The window size
        """
        if self._window is None:
            self._window = self.parser.get_string(self.section,
                                                  ConfigOptions.window_option,
                                                  default=IperfDefaults.window,
                                                  optional=True)
        return self._window

    @property
    def length(self):
        """
        :rtype: String
        :return: The read/write buffer length
        """
        if self._length is None:
            self._length = self.parser.get_string(self.section,
                                                  ConfigOptions.length_option,
                                                  default=IperfDefaults.length,
                                                  optional=True)
        return self._length

    @property
    def parallel(self):
        """
        :return: The number of parallel threads to use
        """
        if self._parallel is None:
            self._parallel = self.parser.get_string(self.section,
                                                    ConfigOptions.parallel_option,
                                                    default=IperfDefaults.parallel,
                                                    optional=True)
        return self._parallel

    @property
    def interval(self):
        """
        :return: The seconds between data reports
        """
        if self._interval is None:
            self._interval = self.parser.get_string(self.section,
                                                    ConfigOptions.interval_option,
                                                    default=IperfDefaults.interval,
                                                    optional=True)
        return self._interval

    @property
    def format(self):
        """
        :return: The output units
        """
        if self._format is None:
            self._format = self.parser.get_string(self.section,
                                                  ConfigOptions.format_option,
                                                  default=IperfDefaults.format,
                                                  optional=True)[0]
        return self._format

    @property
    def time(self):
        """
        :rtype: String Type
        :return: The length of time to run traffic
        """
        if self._time is None:
            self._time = str(self.parser.get_time(self.section,
                                                  ConfigOptions.time_option))
        return self._time

    
    @property
    def client_parameters(self):
        """
        :rtype: IperfClientParameters
        :return: the parameters for the sender
        """
        if self._client_parameters is None:
            self._client_parameters = IperfClientParameters(window=self.window,
                                                            len=self.length,
                                                            parallel=self.parallel,
                                                            interval=self.interval,
                                                            format=self.format,
                                                            time=self.time)
        return self._client_parameters

    @property
    def server_parameters(self):
        """
        :rtype: IperfServerParameters
        :return: The parameters for the receiver
        """
        if self._server_parameters is None:
            self._server_parameters = IperfServerParameters(window=self.window)
        return self._server_parameters

# end class IperfLexicographer
