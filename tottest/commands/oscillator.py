"""
A class to talk to an oscillator.
"""

# tottest modules
from tottest.commons.errors import ConnectionError
from basecommand import BaseThreadedCommand

class Oscillator(BaseThreadedCommand):
    """
    A Class to start and stop an oscillator
    """
    def __init__(self, connection):
        """
        :param:

         - `connection`: connection to oscillation master
        """
        super(Oscillator, self).__init__()
        self.connection = connection
        return

    def run(self):
        """
        :postcondition: oscillate command sent to the oscillator
        """
        output, error = self.connection.oscillate()
        for line in self.generate_output(output, error):
            self.logger.info(line)
        return

    def check_error(self, error):
        """
        Not fully implented yet.

        :param:

         - `error`: stderr file
       
        :raise: CommandError if detected
        """
        line = error.readline()
        if len(line):
            if "pthread_mutex_destroy" in line:
                self.warning("Unable to grab the lock: Is the Oscillator already running?")
            else:
                self.logger.warning(line)
        return

    def generate_output(self, output, error):
        """
        :param:

         - `output`: stdout file
         - `error`: stderr file
        :yield: lines of stdout
        """
        for line in output:
            yield line
        self.check_error(error)
        return
    
    def stop(self):
        """
        :postcondition:

         - `stopped` is True
         - pkill(`oscillate`) called
         - rotate() called
        """
        self.stopped = True
        for line in self.generate_output(*self.connection.pkill('oscillate')):
            self.logger.debug(line)
        for line in self.generate_output(*self.connection.rotate()):
            self.logger.info(line)
        return

    def __del__(self):
        """
        :postcondition: `stop` is called.
        :postcondition: connection is closed
        """
        try:
            self.stop()
            self.connection.client.close()
        except ConnectionError:
            self.logger.debug("Connection Already closed")
        return

# end class Oscillator
