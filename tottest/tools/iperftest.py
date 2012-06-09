"""
A module to hold an iperf test tool
"""

# tottest
from tottest.baseclass import BaseClass
from sleep import Sleep 

class IperfTest(BaseClass):
    """
    The Iperf Test runs a single iperf test.
    """
    def __init__(self, sender, receiver, killers, sleep=None):
        """
        :param:

         - `sender`: IperfCommand configured as sender
         - `receiver`: IperfCommand configured as receiver
         - `killers`: An iterable of Iperf Killers
         - `sleep`: A Sleep object with the sleep time preset
        """
        super(IperfTest, self).__init__()
        self.sender = sender
        self.receiver = receiver
        self.killers = killers
        self._sleep = sleep
        return

    @property
    def sleep(self):
        """
        :return: A sleep
        """
        if self._sleep is None:
            self._sleep = Sleep()
        return self._sleep
    
    def run(self, parameters):
        """
        Runs the test.
        """
        for killer in self.killers:
            self.logger.info(str(killer))
            killer.run()
        self.logger.info("Running Iperf: {0} -> {1}".format(self.sender, self.receiver))
        self.logger.info("Starting the iperf server (receiver)")
        self.receiver.start(parameters.receiver)
        self.logger.info("Sleeping to let the server start.")
        self.sleep.run(parameters.recovery_time)
        self.logger.info("Running the client (sender)")
        self.sender.run(parameters.sender)
        return
# end class IperfTest
