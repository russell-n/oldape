"""
A module to hold a generic iperf command.
"""

from tottest.baseclass import BaseClass
from tottest.commons import errors
from tottest.commons import readoutput
from tottest.threads import threads

ConfigurationError = errors.ConfigurationError

class IperfError(ConfigurationError):
    """
    An IperfError indicates a connection problem.
    """
    
class IperfCommand(BaseClass):
    """
    An Iperf Command executes iperf commands
    """
    def __init__(self, connection, output, parameters=None):
        """
        :param:

         - `connection`: a connection to the device
         - `output`: an output to send data to
         - `parameters`: An IperfParameter to use if none passed to run()
        """
        super(IperfCommand, self).__init__()
        self.connection = connection
        self.output = output
        self.parameters = parameters
        return

    def validate(self, line):
        """
        :param:

         - `line`: a line of output

        :raise: IperfError if an error is detected
        """
        self.logger.debug("Validating: " + line)
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

    def run(self, parameters=None):
        """
        Run the iperf command and send to the output

        :param:

         - `parameters`: A string or IperfParameters to override self.parameters
        """
        if parameters is None:
            parameters = self.parameters
        output, error = self.connection.iperf(str(parameters))
        for line in readoutput.ValidatingOutput(output, self.validate):
            self.output.write(line)

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
        self.thread = threads.Thread(self.run, name='IperfCommand',
                                     args=(parameters,))
        return
# end IperfCommand
