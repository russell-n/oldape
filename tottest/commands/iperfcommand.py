"""
A module to hold a generic iperf command.
"""
import threading

from tottest.baseclass import BaseClass
from tottest.commons import errors
from tottest.commons import readoutput


ConfigurationError = errors.ConfigurationError

class IperfError(ConfigurationError):
    """
    An IperfError indicates a connection problem.
    """
    
class IperfCommand(BaseClass):
    """
    An Iperf Command executes iperf commands
    """
    def __init__(self, connection, output, role, name, parameters=None):
        """
        :param:

         - `connection`: a connection to the device
         - `output`: an output to get writeable files from
         - `parameters`: An IperfParameter to use if none passed to run()
         - `role`: a string to add to the output file to identify it
         - `name` : DUT or TPC
        """
        super(IperfCommand, self).__init__()
        self.connection = connection
        self.output = output
        self.parameters = parameters
        self.role = role
        self.name = name
        return

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
            self.logger.error(line)
            raise IperfError("Another server is already running.")
        return

    def filename(self, parameters):
        """
        If `parameters` has .filename attribute, uses that and adds role:
          <filename>_<role>_{t}
        Else creates a file name to use for output from iperf flags.
           <parameters>_<role>_{t}
           
        :param:

         - `parameters`: The parameters passed in to run.
        """
        try:
            param_string = parameters.filename
        except AttributeError:
            param_string = str(parameters)
            param_string = param_string.replace("-", "")
            param_string = param_string.replace(" ", "_")
        filename = "{param}_{role}_{{t}}".format(param=param_string,
                                                 role=self.role)
        return filename
    
    def run(self, parameters=None):
        """
        Run the iperf command and send to the output

        :param:

         - `parameters`: A string or IperfParameters to override self.parameters

        :postcondition:

         - `Data sent to a file formatted {parameters}_{role}_{timestamp}.iperf
        """
        if parameters is None:
            parameters = self.parameters
        filename = self.filename(parameters)
        file_output = self.output.open(filename=filename,
                                       extension=".iperf")
        output, error = self.connection.iperf(str(parameters))
        for line in readoutput.ValidatingOutput(output, self.validate):
            if "SUM" in line:
                self.logger.info(line.rstrip())
            else:
                self.logger.debug(line)
            file_output.write(line)

        err = error.readline()
        
        if len(err):
            self.validate(err)
            for line in error:
                self.logger.error(line)
                self.validate(line)
        return

    def start(self, parameters=None):
        """
        :param:

         - `parameters`: A parameters string or object to send to iperf
        """
        
        self.thread = threading.Thread(target=self.run, name='IperfCommand',
                                     args=(parameters,))
        self.thread.daemon = True
        self.thread.start()
        return

    def __str__(self):
        return self.name
# end IperfCommand
