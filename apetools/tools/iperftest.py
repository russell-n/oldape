
# apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import CommandError
from apetools.commands.sftpcommand import SftpCommand

#this folder
from sleep import Sleep 
from killall import KillAll, KillAllError



SIGKILL = 9


class IperfTestError(CommandError):
    """
    A error to raise if there was an iperf-specific problem
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

    def kill_processes(self, connection):
        """
        Kills iperf processes over the connection

         * If the default level fails, tries a -9

        :param:

         - `connection`: connection to the host for the KillAll
        """
        self.kill.level = None
        self.kill.connection = connection

        try:
            self.kill()
        except KillAllError as error:
            self.logger.warning(error)
            self.kill.level = SIGKILL
            self.kill()            
        return
    
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
        self.kill_processes(sender.connection)
        self.kill_processes(receiver.connection)
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

        # This was added to force the dumping of UDP server output
        self.logger.info("Sleeping to let the server finish its output.")
        self.sleep()
        self.logger.info("Killing the server on {0}".format(receiver.connection.hostname))
        self.kill_processes(receiver.connection)

        # this is a quick hack to get the ipad working
        # it needs somehing more elegant
        if self.receiver_command.is_daemon:
            target = self.receiver_command.get_output_filename()
            if target is None:
                self.logger.warning("Unable to get the server-side filename to copy")
            sftp = SftpCommand(connection=self.receiver_command.device.connection)
            sftp.get(self.receiver_command.last_filename, target)

        #self.receiver_command.abort()
        return
# end class IperfTest
