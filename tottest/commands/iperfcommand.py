"""
A module to hold a generic iperf command.
"""
import threading
import time

from tottest.baseclass import BaseClass
from tottest.devices.basedevice import BaseDeviceEnum
from tottest.commons import errors
from tottest.commons import readoutput
from tottest.pipes.storagepipe import StoragePipe, StoragePipeEnum
from tottest.parsers.sumparser import SumParser
ConfigurationError = errors.ConfigurationError
CommandError = errors.CommandError

EOF = ""
NEWLINE = "\n"


class IperfError(CommandError):
    """
    An IperfError indicates a connection problem.
    """
# end class IperfError
    
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
        self.parameters = parameters
        self._parser  = None
        self._output = None
        self.output = output
        self.base_filename = base_filename
        self.output.extend_path(subdirectory) 

        self.role = role
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
        if self._parser is None and hasattr(self.parameters, "time"):
            threads = None
            if self.parameters.parallel is not None:
                threads = int(self.parameters.parallel.split()[-1])
            parser = SumParser(threads=threads)
            self._parser = StoragePipe(role=StoragePipeEnum.sink,
                                       transform=parser)            
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
            if hasattr(self.parameters, "time"):
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
        if self.role == IperfCommandEnum.client:
            filename = self.base_filename
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
            if hasattr(self.parameters, "time"):
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
        return

    def abort(self):
        """
        :postcondition: self.stop is True      
        """
        self.stop = True
        return
    
    def run(self, device, filename):
        """
        Run the iperf command and send to the output

        :param:

         - `device`: A device to issue the command on
         - `filename`: a base-name to use for the output file.

        :raise: IperfError if runtime is greater than self.parameters.time
        """
        filename = self.filename(filename, device.role)
        file_output = self.output.open(filename=filename)

        self.logger.debug("Executing parameters: {0}".format(self.parameters))
        output, error = device.connection.iperf(str(self.parameters))
        
        start_time = time.time()
        abort_time = start_time + self.max_time
        self.running = True 
        for line in readoutput.ValidatingOutput(output, self.validate):
            self.logger.debug(line.rstrip(NEWLINE))
            try:
                #if "SUM" in line:
                 #   import pudb; pudb.set_trace()
                file_output.send(line)
            except StopIteration:
                self.logger.debug("End Of File Reached")
                break
            if self.now() > abort_time:
                try:
                    output.send(EOF)
                except StopIteration:
                    pass
                self.abort = False
                self.running = False
                raise IperfError("Expected runtime: {0} Actual: {1} (aborting)".format(self.parameters.time,
                                                                                       self.now() - start_time))
            if self.stop:
                try:
                    file_output.send(EOF)
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
        self.thread = threading.Thread(target=self.run, name='IperfCommand',
                                     args=(device, filename))
        self.thread.daemon = True
        self.thread.start()
        return

    def __str__(self):
        return self.name
# end IperfCommand
