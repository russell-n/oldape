"""
A module to hold a generic iperf command.
"""
#python standard library
import threading
import time
import os

#apetools
from apetools.baseclass import BaseThreadClass
from apetools.devices.basedevice import BaseDeviceEnum
from apetools.commons import errors
from apetools.commons import readoutput
from apetools.pipes.storagepipe import StoragePipe, StoragePipeEnum
from apetools.parsers.sumparser import SumParser
from apetools.parameters.iperf_common_parameters import IperfParametersEnum

ConfigurationError = errors.ConfigurationError
CommandError = errors.CommandError

class IperfError(CommandError):
    """
    An IperfError indicates a connection problem.
    """
# end class IperfError
    
class IperfCommandError(ConfigurationError):
    """
    an error to raise if the settings are unknown
    """
# end class IperfCommandError
    

class IperfCommandEnum(object):
    __slots__ = ()
    client = "client"
    server = "server"
    time = 'time'
    eof = ""
    newline = "\n"
    udp = 'udp'
    path = 'path'
    iperf = 'iperf'
# end IperfCommandEnum
    
    
class IperfCommand(BaseThreadClass):
    """
    An Iperf Command executes iperf commands
    """
    def __init__(self, parameters, output, role, base_filename="", subdirectory="raw_iperf"):
        """
        :param:

         - `parameters`: An IperfParameter to use
         - `output`: A Storage Pipe
         - `role`: client or server
         - `base_filename`: string to add to all filenames
         - `subdirectory`: A folder to put the iperf files intn
        """
        super(IperfCommand, self).__init__()
        self.role = role
        self.parameters = parameters
        self._parser  = None
        self._output = None
        self.output = output
        self.base_filename = base_filename
        self.output.extend_path(subdirectory) 

        self._max_time = None
        self._now = None

        self.running = False
        self.stop = False
        return

    @property
    def parser(self):
        """
        :return: SumParser pipeline (if this is the client)
        """
        if self._parser is None:
            threads = None
            if self.parameters.parallel is not None:
                threads = int(self.parameters.parallel.split()[-1])
            parser = SumParser(threads=threads)
            self._parser = StoragePipe(role=StoragePipeEnum.sink,
                                       transform=parser,
                add_timestamp=True)            
        return self._parser
    @property
    def output(self):
        """
        :return: the storage pipeline for raw iperf output
        """        
        return self._output

    @output.setter
    def output(self, out):
        """
        :param:

         - `out`: an output pipeline object
        """
        if self.parser is not None:
            self.parser.path = out.path
            self.parser.extend_path("parsed")
            out.target = self.parser
            out.role = StoragePipeEnum.start
        self._output = out
        return

    @property
    def now(self):
        """
        :return: time-function to check for timeouts
        """
        if self._now is None:
            if self.role == IperfCommandEnum.client:
                self._now = time.time
            else:
                self._now = lambda: 0
        return self._now

    def filename(self, filename, node_type):
        """
        :param:

         - `filename`: base filename to add prefix to
         - `node_type`: the device.role
         
        :return: a prefix to add to the filename given
        :raise: ConfigurationError if self.role or node_type are unknown
        """
        if hasattr(self.parameters, IperfParametersEnum.udp):
            filename = "udp_" + filename
        else:
            filename = "tcp_" + filename
        if self.role == IperfCommandEnum.client:
            filename = self.base_filename + filename
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
            self._max_time = 0
            if hasattr(self.parameters, IperfCommandEnum.time):
                self._max_time = max(120, 1.5 * float(self.parameters.time.split()[-1]))
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
        elif "connect failed" in line:
            self.logger.error(line)
            raise IperfError("Client Unable to connect ({0})".format(line))
        return

    def abort(self):
        """
        :postcondition: self.stop is True      
        """
        self.stop = True
        return
    
    def run(self, device, filename, server=False):
        """
        Run the iperf command and send to the output

        :param:

         - `device`: A device to issue the command on
         - `filename`: a base-name to use for the output file.

        :raise: IperfError if runtime is greater than self.parameters.time
        """
        filename = self.filename(filename, device.role)
        is_udp = hasattr(self.parameters, IperfCommandEnum.udp)
        
        if not server:
            if not is_udp:
                self.output.set_emit()
            else:
                self.output.unset_emit()
        else:
            if is_udp:
                self.output.set_emit()
            else:
                self.output.unset_emit()
                 
        file_output = self.output.open(filename=filename)
        
        self.logger.debug("Executing parameters: {0}".format(self.parameters))
        
        with device.connection.lock:
            self.logger.debug("Waiting for the connection lock")
            self.logger.info("running iperf {0}".format(self.parameters))
            output, error = device.connection.iperf(str(self.parameters))
            self.logger.debug("Out of the connection lock")
        start_time = time.time()
        abort_time = start_time + self.max_time
        self.running = True
        newline = IperfCommandEnum.newline
        end_of_file = IperfCommandEnum.eof
        for line in readoutput.ValidatingOutput(output, self.validate):
            if len(line.strip()):
                self.logger.debug(line.rstrip(newline))
            try:
                file_output.send(line)
            except StopIteration:
                self.logger.debug("End Of File Reached")
                break
            if self.now() > abort_time:
                try:
                    file_output.send(end_of_file)
                except StopIteration:
                    pass
                self.abort = False
                self.running = False
                raise IperfError("Expected runtime: {0} Actual: {1} (aborting)".format(self.parameters.time,
                                                                                       self.now() - start_time))
            if self.stop:
                try:
                    file_output.send(end_of_file)
                except StopIteration:
                    pass
                self.stop = False
                self.logger.debug("Aborting")
                break
        
        self.running = False
        
        
        err = error.readline()
        
        if len(err):
            self.validate(err)
        return

    def start(self, device, filename):
        """
        :param:

         - `device`: device to issue the iperf command
         - `filename`: base filename to use for output file

        :postcondition: iperf command started in thread
        """
        self.thread = threading.Thread(target=self.run_thread, name='IperfCommand',
                                       kwargs={'device':device,
                                               'filename':filename,
                                               'server':True})
        self.thread.daemon = True
        self.thread.start()
        return

    def __str__(self):
        return self.name
# end IperfCommand
