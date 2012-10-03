"""
A module to hold an iperf test tool
"""

# tottest
from tottest.baseclass import BaseClass

#this folder
from sleep import Sleep 
from killall import KillAll


class IperfTest(BaseClass):
    """
    The Iperf Test runs a single iperf test.
    """
    def __init__(self, sender_command=None, receiver_command=None, sleep=None):
        """
        :param:

         - `sender_command`: an IperfCommand bundled with client parameters
         - `receiver_command`: IperfCommand bundled with server parameters
         - `sleep`: A Sleep object with the sleep time preset
        """
        super(IperfTest, self).__init__()
        self.sender_command = sender_command
        self.receiver_command = receiver_command        
        self._sleep = sleep
        self._kill = None
        return

    @property
    def kill(self):
        """
        :return: iperf process killer
        """
        if self._kill is None:
            self._kill = KillAll(name="iperf")
        return self._kill

    @property
    def sleep(self):
        """
        :return: A sleep
        """
        if self._sleep is None:
            self._sleep = Sleep()
        return self._sleep
    
    def run(self, sender, receiver, filename):
        """
        Runs the test.

        :param:

         - `sender`: a device to originate traffic
         - `receiver`: A device to receive traffic
         - `filename`: a filename to use for output
        """
        self.kill(sender.connection)
        self.kill(receiver.connection)
        self.logger.info("Running Iperf: {0} -> {1}".format(self.sender.address, self.receiver.address))
        self.logger.info("Starting the iperf server (receiver)")
        self.receiver_command.start(receiver, filename)
        self.logger.info("Sleeping to let the server start.")
        self.sleep()
        self.logger.info("Running the client (sender)")
        self.sender_command.run(sender, filename)
        return
# end class IperfTest
