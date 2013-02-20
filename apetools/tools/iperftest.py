"""
A module to hold an iperf test tool
"""
# apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError

#this folder
from sleep import Sleep 
from killall import KillAll

class IperfTestError(CommandError):
    """
    """
# end class IperfTestError


class IperfTest(BaseClass):
    """
    The Iperf Test runs a single iperf test.
    """
    def __init__(self, sender_command=None, receiver_command=None, sleep=None,
                 wait_events=None):
        """
        :param:

         - `sender_command`: an IperfCommand bundled with client parameters
         - `receiver_command`: IperfCommand bundled with server parameters
         - `sleep`: A Sleep object with the sleep time preset
         - `wait_events`: list of events to wait for
        """
        super(IperfTest, self).__init__()
        self.sender_command = sender_command
        self.receiver_command = receiver_command
        self.wait_events = wait_events
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
            self._sleep = Sleep(1)
        return self._sleep
    
    def __call__(self, sender, receiver, filename):
        """
        Runs the test.

        :param:

         - `sender`: a device to originate traffic
         - `receiver`: A device to receive traffic
         - `filename`: a filename to use for output

        :raise: IperfTestError if wait_events time out
        """
        # set the target address in the iperf command to the receiver (server)
        self.sender_command.parameters.client = receiver.address

        self.logger.info("Killing Existing Iperf Processes")
        self.kill(sender.connection)
        self.kill(receiver.connection)
        self.logger.info("Running Iperf: {2} ({0}) -> {3} ({1})".format(sender.address, receiver.address,
                                                                        sender.role, receiver.role))
        self.logger.info("Starting the iperf server (receiver)")

        self.receiver_command.start(receiver, filename)
        self.logger.info("Sleeping to let the server start.")
        self.sleep()

        # allow other processes to block the iperf client-start
        if self.wait_events is not None:
            time_out = self.sender_command.max_time
            if not self.wait_events.wait(time_out):
                raise IperfTestError("Timed out waiting for event.")                
        self.logger.info("Running the client (sender)")

        self.sender_command.run(sender, filename)
        if self.receiver_command.running:
            self.receiver_command.abort()
        return
# end class IperfTest
