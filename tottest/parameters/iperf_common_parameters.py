"""
A module to hold iperf parameter classes

Names of parameters match the long-options given to iperf :

    e.g. --port becomes IperfCommonParameters.port

and the doc-strings cross-reference them as the short form (-p)
"""
#python
import re
from types import BooleanType

#tottest
from tottest.baseclass import BaseClass
from tottest.commons import errors
from tottest.commons import expressions



ConfigurationError = errors.ConfigurationError

SPACE = ' '
UNDERSCORE = "_"

VALID_BUFFER_LENGTHS = expressions.REAL + expressions.CLASS.format("KM") + expressions.ZERO_OR_ONE + expressions.WORD_ENDING + expressions.LINE_ENDING
VALID_FORMATS = 'b k m K M'.split()
MAXIMUM_PORT = 65535
MINIMUM_PORT = 1
LOWEST_PORT = 1024
VALID_OUTPUT = expressions.NOT_SPACE + expressions.ONE_OR_MORE + expressions.WORD_ENDING
VALID_EXCLUDES = expressions.CLASS.format("CDMSV") + expressions.ONE_OR_MORE + expressions.WORD_ENDING
VALID_REPORT_STYLES = "cC"

class IperfParametersEnum(object):
    """
    A holder for Iperf Parameter Constants
    """
    __slots__ = ()
    udp = "udp"
    tcp = "tcp"
# end class IperfParametersEnum

class IperfCommonParameters(BaseClass):
    """
    Iperf Common Parameters are common to all Iperf commands.
    """
    _block_attributes = False
    def __init__(self):
        super(IperfCommonParameters, self).__init__()
        self._logger = None
        self._format = None
        self._interval = None
        self._len = None
        self._output = None
        self._port = None
        self._bind = None
        self._compatibility = None
        self._ipv6version = None
        self._reportexclude = None
        self._reportstyle = None
        self._parameter_names = None
        self._block_attributes = True
        return

    @property
    def format(self):
        """
        :return: the format parameter (--f [bkmKM])
        """
        return self._format

    @format.setter
    def format(self, new_format):
        """
        :param:

         - `format`: one of {b, k, m, K, M}
        """
        if new_format not in VALID_FORMATS:
            raise errors.ConfigurationError("Invalid format: {0} (must be 'b', 'k', 'm', 'K', or 'M')".format(new_format))
        self._format = "--format {0}".format(new_format)
        return

    @property
    def interval(self):
        """
        :return: The time between data reports (-i <seconds>)
        """
        return self._interval

    @interval.setter
    def interval(self, new_interval):
        """
        :param:

         - `new_interval`: something that can be cast to a float.
        """
        try:
            if re.search(expressions.INTEGER, str(new_interval)):
                self._interval = "--interval {0}".format(new_interval)
            else:
                self._interval = "--interval {0:.1f}".format(float(new_interval))
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError("Invalid Interval: {0}".format(new_interval))
        return
    
    @property
    def len(self):
        """
        :return: The length of the read-write-buffer (-l [KM])
        """
        return self._len

    @len.setter
    def len(self, new_len):
        """
        :param:

         - `new_len`: Buffer Length (format 'n[KM]')
        """
        if not re.match(VALID_BUFFER_LENGTHS, str(new_len)):
            raise ConfigurationError("Invalid Buffer Length: {0}".format(new_len))
        self._len = "--len {0}".format(new_len)
        return

    @property
    def output(self):
        """
        :return: The name iperf should use as the file-name (-o <filename>)
        """
        return self._output

    @output.setter
    def output(self, name):
        """
        :param:

         - `name`: A valid file name (so just about anything (but no spaces)).
        """
        if SPACE in name:
            raise ConfigurationError("Output Name ({0}) can't have spaces".format(name))
        self._output = "--output {0}".format(name)
        return

    @property
    def port(self):
        """
        :return: The network port the server is (will be) using (-p <port>)
        """
        return self._port

    @port.setter
    def port(self, new_port):
        """
        :param:

         - `new_port`: a valid network port 1 - 65535

        :warns: if port is less than 1024 (reserved in Unix)
        :raises: configuration error if 65535 < port < 1
        """
        try:
            new_port = int(new_port)
            if MAXIMUM_PORT < new_port or new_port < MINIMUM_PORT:
                raise ConfigurationError("Port {0} out of range".format(new_port))
            if new_port < LOWEST_PORT:
                self.logger.warning("Port {0} is within well-known ports range (1-1023)".format(new_port))
            self._port = "--port {0}".format(new_port)
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError("Invalid port: {0}".format(new_port))
        return
    
    @property
    def bind(self):
        """
        :return: The host to bind to. (-B <host>)
        """
        return self._bind

    @bind.setter
    def bind(self, hostname):
        """
        :param:

         - `hostname`: A valid hostname 
        """
        self._bind = "--bind {0}".format(hostname)
        return

    @property
    def compatibility(self):
        """
        :return: backwards-compatability flag (-C)
        """
        return self._compatibility

    @compatibility.setter
    def compatibility(self, set_compatible):
        """
        :param:

         - `set_compatible`: A boolean which if True sets the flag
        """
        if not type(set_compatible) is BooleanType:
            raise ConfigurationError("{0} must be True or False")
        if set_compatible:
            self._compatibility = '--compatibility'
        return
        
    @property
    def ipv6version(self):
        """
        :return: The flag to indicate IPv6 is being used (-V).
        """
        return self._ipv6version

    @ipv6version.setter
    def ipv6version(self, set_to_ipv6):
        """
        :param:

         - `set_to_ipv6`: A boolean which if True, sets the IPv6Version flag.
        """
        if type(set_to_ipv6) is not BooleanType:
            raise ConfigurationError("{0} must be True or False".format(set_to_ipv6))
        if set_to_ipv6:
            self._ipv6version = "--IPv6Version"
        return
    
    @property
    def reportexclude(self):
        """
        :return: The report exclude flags (-x [CDMSV])

         * C - Connection
         * D - Data
         * M - Mutlicast
         * S - Settings
         * V - serVer reports
        """
        return self._reportexclude

    @reportexclude.setter
    def reportexclude(self, exclude_flags):
        """
        :param:

         - `exclude_flags`: a subset of CDMSV
        """
        if not re.match(VALID_EXCLUDES, exclude_flags):
            raise ConfigurationError("{0} must only contain a subset of CDMSV".format(exclude_flags))
        self._reportexclude = "--reportexclude {0}".format(exclude_flags)
        return
    
    @property
    def reportstyle(self):
        """
        :return: The output-to-csv flag (-y C|c)
        """
        return self._reportstyle

    @reportstyle.setter
    def reportstyle(self, csv_flag):
        """
        :param:

         - `csv_flag`: in {c, C}
        """
        if csv_flag not in VALID_REPORT_STYLES:
            raise ConfigurationError("Invalid report-style: {0} (should be 'c' or 'C')".format(csv_flag))
        self._reportstyle = "--reportstyle {0}".format(csv_flag)

    @property
    def parameter_names(self):
        """
        :return: a list of valid parameter names
        """
        if self._parameter_names is None:
            self._parameter_names = [field for field in dir(self) if not field.startswith("_") and field not in ("parameter_names","logger")]
        return self._parameter_names

    def __str__(self):
        """
        :return: string of set flags in alphabetical order (of the flags, not the values)
        """
        non_parameters = ("_block_attributes" , "_logger")
        keys = (key for key in sorted(self.__dict__.keys()) if key not in non_parameters)
        values = (getattr(self, key.lstrip(UNDERSCORE)) for key in keys)
        filtered_values = (value for value in values if value is not None)
        return SPACE.join(filtered_values)

    def __setattr__(self, key, value):
        """
        Overrides the setattr to add a freeze to prevent accidentally adding attributes.
        """
        if self._block_attributes and not hasattr(self, key):
            raise ConfigurationError("Unknown Attribute: {0}".format(key))
        super(IperfCommonParameters, self).__setattr__(key, value)
        return
# end class IperfCommonParameters
