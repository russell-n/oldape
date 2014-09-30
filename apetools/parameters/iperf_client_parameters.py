
#python
from types import BooleanType
import re

# apetools
from iperf_common_tcp_parameters import IperfCommonTcpParameters
from iperf_common_parameters import VALID_BUFFER_LENGTHS as VALID_BYTES
from iperf_common_parameters import MAXIMUM_PORT, MINIMUM_PORT, LOWEST_PORT, IperfParametersEnum

from apetools.commons import errors, expressions


ConfigurationError = errors.ConfigurationError

VALID_TIME_INTEGER = re.compile(expressions.INTEGER + expressions.WORD_ENDING +
                                expressions.SPACES_OPTIONAL +
                                expressions.LINE_ENDING)
VALID_TIME_FLOAT = re.compile(expressions.FLOAT + expressions.WORD_ENDING +
                              expressions.SPACES_OPTIONAL+
                              expressions.LINE_ENDING)

VALID_BANDWIDTHS = VALID_BYTES

SPACE = ' '


class IperfTcpClientParameters(IperfCommonTcpParameters):
    """
    IperfTcpClientParameters holds parameters used by Iperf TCP clients
    """
    def __init__(self):
        super(IperfTcpClientParameters, self).__init__()
        self._block_attributes = False
        self._client = None
        self._dualtest = None
        self._fileinput = None
        #self._linux_congestion = None
        self._listenport = None
        self._num = None
        self._parallel = None
        #self._stdin = None
        self._time = None
        self._tradeoff = None
        self._ttl = None
        self._block_attributes = True
        return

    @property
    def client(self):
        """
        :return: client flag (-c <hostname>)
        """
        return self._client

    @client.setter
    def client(self, hostname):
        """
        :param:

         - `hostname`: The hostname of the server
        """
        if any((hostname is None, not len(hostname), SPACE in hostname)):
            raise ConfigurationError("Invalid hostname: {0}".format(hostname))
        self._client = "--client {0}".format(hostname)
        return

    @property
    def dualtest(self):
        """
        :return: The dualtest flag (-d)
        """
        return self._dualtest

    @dualtest.setter
    def dualtest(self, set_dualtest):
        """
        :param:

         - `set_dualtest`: A boolean which if True sets the dualtest flag
        """
        if type(set_dualtest) is not BooleanType:
            raise ConfigurationError("set_dualtest must be boolean, not {0}".format(set_dualtest))
        if set_dualtest:
            self._dualtest = "--dualtest"
        return

    @property
    def fileinput(self):
        """
        :return: '--fileinput <filename>' 
        """
        return self._fileinput

    @fileinput.setter
    def fileinput(self, filename):
        """
        :param:

         - `filename`: The name of the file to use as input
        """
        filename = filename.strip()
        if SPACE in filename:
            raise ConfigurationError("No spaces allowed in filename - {0}".format(filename))
        self._fileinput = "--fileinput {0}".format(filename)
        return

    @property
    def listenport(self):
        """
        :return: The listenport flag (-L <port>)  
        """
        return self._listenport

    @listenport.setter
    def listenport(self, port):
        """
        :param:

         - `port`: A network port to listen on for bidirectional test.
        """
        try:
            port = int(port)
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError("{0} not castable to an integer".format(port))
        if MAXIMUM_PORT < port or port < MINIMUM_PORT:
            raise ConfigurationError("{0} outside of valid port range ({1} to {2})".format(port, MINIMUM_PORT, MAXIMUM_PORT))
        if port < LOWEST_PORT:
            self.logger.warning("{0} is within the well-known ports range ({1} to {2})".format(port, MINIMUM_PORT, LOWEST_PORT))
            
        self._listenport = "--listenport {0}".format(int(port))
        return 
    
    @property
    def num(self):
        """
        :return: The number of bytes to send flag (-n <bytes>[KM])
        """
        return self._num

    @num.setter
    def num(self, num_bytes):
        """
        :param:

         - `num_bytes`: Number of bytes to send
        """
        if not re.match(VALID_BYTES, num_bytes):
            raise ConfigurationError("num_bytes must be formatted n[KM], not {0}".format(num_bytes))
        self._num = "--num {0}".format(num_bytes)
        return

    @property
    def time(self):
        """
        :return: The time flag (-t <seconds>)
        """    
        return self._time

    @time.setter
    def time(self, new_time):
        """
        :param:

         - `new_time`: time in seconds (floats are rounded to 1 decimal place)
        """
        new_time = str(new_time)
        if VALID_TIME_INTEGER.match(new_time):
            self._time = "--time {0}".format(new_time)
        elif VALID_TIME_FLOAT.match(new_time):
            self._time = "--time {0:.1f}".format(float(new_time))
        else:
            raise ConfigurationError("Time must be an integer or float not {0}".format(new_time))
        return
    
    @property
    def tradeoff(self):
        """
        :return: the Tradeoff flag (-r)
        """
        return self._tradeoff

    @tradeoff.setter
    def tradeoff(self, set_tradeoff):
        """
        :param:

         - `set_tradeoff`: A Boolean which if True sets the tradeoff flag.
        """
        if not type(set_tradeoff) is BooleanType:
            raise ConfigurationError("set_tradeoff must be boolean, not {0}".format(set_tradeoff))
        if set_tradeoff:
            self._tradeoff = "--tradeoff"
        return

    @property
    def ttl(self):
        """
        :return: The time-to-live flag (-T <hops>)
        """        
        return self._ttl

    @ttl.setter
    def ttl(self, hops):
        """
        :param:

         - `hops`: The time-to-live
        """
        try:
            hops = int(hops)
        except ValueError as error:
            self.logger.error(error)
            raise ConfigurationError("ttl must be an integer, not '{0}'".format(hops))
        self._ttl = "--ttl {0}".format(hops)
        return
# end class IperfTcpClientParameters


class IperfUdpClientParameters(IperfTcpClientParameters):
    """
    IperfUdpClientParameters is a superset of the IperfTcpClientParameters.
    Adds udp and bandwidth.
    """
    def __init__(self):
        super(IperfUdpClientParameters, self).__init__()
        self._block_attributes = False
        self._bandwidth = None
        self.udp = "--udp"
        self._block_attributes = True
        return

    @property
    def bandwidth(self):
        """
        :return: The udp bandwidth flag (-b n[KM])
        """        
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, new_bandwidth):
        """
        :param:

         - `new_bandwidth`: the bandwidth to set
        """
        if not re.match(VALID_BANDWIDTHS, new_bandwidth):
            raise ConfigurationError("Invalid Bandwidth: {0}".format(new_bandwidth))
        self._bandwidth = "--bandwidth {0}".format(new_bandwidth)
        return
# end class IperfUdpClientParameters


client_parameters = {IperfParametersEnum.tcp: IperfTcpClientParameters,
                     IperfParametersEnum.udp: IperfUdpClientParameters}
