
#python Libraries
import time
# apetools Libraries
from apetools.baseclass import BaseClass


UNKNOWN_HOST = 'unknown host'
NEWLINE = "\n"


class BusyboxWget(BaseClass):
    """
    Does a wget and times it.
    """
    def __init__(self, target=None, connection=None, timeout=2, output='/dev/null'):
        """
        BusyboxWget Constructor
        
        :param:

         - `target`: A URL to pull from
         - `connection`: A Connection to the device
         - `timeout`: amount of time to wait before timing out
         - `output`: place to send the output of the http pull
        """
        super(BusyboxWget, self).__init__()
        self.target = target
        self.connection = connection
        self.timeout = timeout
        self.output = output        
        self._arguments = None
        self._expression = None
        return

    @property
    def arguments(self):
        """
        :return: The busybox arguments to use
        """
        if self._arguments is None:
            self._arguments = "wget {0} -O {1} -T {2}".format(self.target,
                                                                      self.output,
                                                                      self.timeout)
        return self._arguments
    
    def run(self):
        """
        Executes a single wget

        :return: PingData or None
        """
        start = time.time()
        output, error = self.connection.busybox(self.arguments, timeout=1)
        elapsed = time.time() - start
        self.logger.info("Wget Elapsed Time: {0} seconds".format(elapsed))
        for line in output:
            self.logger.debug(line.rstrip(NEWLINE))
        err = error.readline()
        if len(err):
            self.logger.error(err)
        return

    def __call__(self, parameters=None):
        """
        Executes a single ping, checks for a success, returns ping data if it succeeds.

        
        :return: PingData or None
        :raise: ConfigurationError if the target is unknown
        """
        self.run()
        return
# end class BusyboxWget
