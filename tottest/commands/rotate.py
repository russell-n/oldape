"""
A command-line interface to run the rotate command remotely.
"""

from tottest.baseclass import BaseClass
from tottest.commons.errors import ConfigurationError
from tottest.commons.errors import CommandError

class RotateCommand(BaseClass):
    """
    A class to issue a remote 
    """
    def __init__(self, connection):
        """
        :param:

         - `connection`: A connection to the controller of the rate-table (rotator)
        """
        super(RotateCommand, self).__init__()
        self.connection = connection
        return

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: namedtuple with parameters.angles.parameters
        """
        angle, velocity = parameters.angle_velocity.parameters
        arguments = "{0} --velocity {1}".format(angle, velocity)
        stdout, stderr = self.connection.rotate(arguments)
        for line in stdout:
            self.logger.debug(line)
        for line in stderr:
            if len(line) > 1:
                self.logger.error(line)
            if "Requested position is out of range." in line:
                raise ConfigurationError("Requested rotation angle of {0} is out of range".format(parameters.angles.parameters))
        return

    def check_errors(self, line):
        """
        :param:

         - `line`: line of output from the rotate command

        :raise: CommandError if a known fatal error is detected
        """
        if "No such file or directory" in line:
            raise CommandError("The Rotator was not found -- is the USB cable plugged in?")
        return
# end class RotateCommand


if __name__ == "__main__":
    import time
    from tottest.connections.sshconnection import SSHConnection
    c = SSHConnection("pogo2", "root")
    r = RotateCommand(c)
    print "Rotate to 90 degrees"
    r(90)
    time.sleep(1)
    print "Rotate to 180 Degrees"
    r(180)
    time.sleep(1)
    print "Rotate to 0 degrees"
    r()
