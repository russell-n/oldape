"""
A module to hold client-specific parameters.
"""

#python
from types import BooleanType
import re

# tottest
from iperf_common_tcp_parameters import IperfCommonTcpParameters
from iperf_common_parameters import VALID_BUFFER_LENGTHS as VALID_BYTES
from tottest.commons import errors, expressions

ConfigurationError = errors.ConfigurationError

VALID_TIME_INTEGER = re.compile(expressions.INTEGER + expressions.WORD_ENDING +
                                expressions.SPACES_OPTIONAL +
                                expressions.LINE_ENDING)
VALID_TIME_FLOAT = re.compile(expressions.FLOAT + expressions.WORD_ENDING +
                              expressions.SPACES_OPTIONAL+
                              expressions.LINE_ENDING)
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
        #self._linux_confgestion = None
        #self._listenport = None
        self._num = None
        #self._parallele = None
        #self._stdin = None
        self._time = None
        self._tradeoff = None
        #self._ttl = None
        return

    @property
    def client(self):
        """
        :return: client flag
        """
        return self._client

    @client.setter
    def client(self, hostname):
        """
        :param:

         - `hostname`: The hostname of the server
        """
        self._client = "--client {0}".format(hostname)
        return

    @property
    def dualtest(self):
        """
        :return: The dualtest flag
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
        :return: The --fileinput flag
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
    def num(self):
        """
        :return: The number of bytes to send flag
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
        :return: The --time flag
        """    
        return self._time

    @time.setter
    def time(self, new_time):
        """
        :param:

         - `new_time`: time in seconds (floats are rounded to 1 decimal place)
        """
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
        :return: the Tradeoff flag
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
# end class IperfTcpClientParameters
