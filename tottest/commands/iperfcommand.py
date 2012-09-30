"""
A module to hold a generic iperf command.
"""
import threading
from time import time as now
from sys import maxint

from tottest.baseclass import BaseClass
from tottest.devices.basedevice import BaseDeviceEnum
from tottest.commons import errors
from tottest.commons import readoutput


ConfigurationError = errors.ConfigurationError
CommandError = errors.CommandError


class IperfError(CommandError):
    """
    An IperfError indicates a connection problem.
    """
class IperfCommandError(ConfigurationError):
    """
    an error to raise if the settings are unknown
    """
    
class IperfCommandEnum(object):
    __slots__ = ()
    client = "client"
    server = "server"
     
class IperfCommand(BaseClass):
    """
    An Iperf Command executes iperf commands
    """
    def __init__(self, parameters, output, role):
        """
        :param:

         - `output`: an output to get writeable files from
         - `parameters`: An IperfParameter to use 
         - `role`: client or server
        """
        super(IperfCommand, self).__init__()
        self.output = output
        self.parameters = parameters
        self.role = role
        self._max_time = None
        return

    def filename(self, filename, node_type):
        """
        :param:

         - `filename`: base filename to add prefix to
         - `node_type`: the device.role
         
        :return: a prefix to add to the filename given
        :raise: ConfigurationError if self.role or node_type are unknown
        """
        if self.role == IperfCommandEnum.client:
            if node_type == BaseDeviceEnum.node:
                return "sent_from_node_" + filename
            elif node_type == BaseDeviceEnum.tpc:
                return "sent_to_node_" + filename
            else:
                raise IperfCommandError("Unknown device.role: '{0}'".format(node_type))
        elif self.role == IperfCommandEnum.server:
            if node_type == BaseDeviceEnum.node:
                return "received_by_node_" + filename
            elif node_type == BaseDeviceEnum.tpc:
                return "received_by_tpc_" + filename
            else:
                raise IperfCommandError("Unknown device.role: '{0}'".format(node_type))
        raise IperfCommandError("Unknown Iperf Role: '{0}'".format(self.role))
        return 

    @property
    def max_time(self):
        """
        :return: the maximum amount of time to run
        """
        if self._max_time is None:
            self._max_time = maxint
            if hasattr(self.parameters, "time"):
                self._max_time = max(120, 1.2 * float(self.parameters.time.split()[-1]))
        return self._max_time
    
    def validate(self, line):
        """
        :param:

         - `line`: a line of output

        :raise: IperfError if an error is detected
        """
        #self.logger.debug("Validating: " + line)
        if "No route to host" in line:
            self.logger.error(line)
            raise IperfError("Unable to connect to host")
        elif "Connection refused" in line:
            self.logger.error(line)
            raise IperfError("Iperf server not running on remote host")
        elif "Address already in use" in line:
            self.logger.warning(line)
            #raise IperfError("Another server is already running.")
        return
    
    def run(self, device, filename):
        """
        Run the iperf command and send to the output

        :param:

         - `device`: A device to issue the command on
         - `filename`: a base-name to use for the output file.
        """
        filename = self.filename(filename)
        file_output = self.output.open(filename=filename,                                       
                                       subdir="raw_iperf")
        output, error = self.connection.iperf(str(self.parameters))
        start_time = now()
        abort_time = start_time + self.max_time

        for line in readoutput.ValidatingOutput(output, self.validate):
            if "SUM" in line or "-1" in line:
                self.logger.info(line.rstrip())
            else:
                self.logger.debug(line)
            file_output.write(line)
            if now() > abort_time:
                raise IperfError("Expected runtime: {0} Actual: {1} (aborting)".format(self.parameters.time, now() - start_time))

        err = error.readline()
        
        if len(err):
            self.validate(err)
            for line in error:
                self.logger.error(line)
                self.validate(line)
        return

    def start(self, device, filename):
        """
        :param:

         - `device`: device to issue the iperf command
         - `filename`: base filename to use for output file

        :postcondition: iperf command started in thread
        """
        self.thread = threading.Thread(target=self.run, name='IperfCommand',
                                     args=(device, filename))
        self.thread.daemon = True
        self.thread.start()
        return

    def __str__(self):
        return self.name
# end IperfCommand
