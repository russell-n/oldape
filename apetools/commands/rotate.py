"""
A command-line interface to run the rotate command remotely.
"""

from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commons.errors import CommandError
from apetools.tools.killall import KillAll



class RotateError(CommandError):
    """
    An error in the rotation
    """
# end class RotateError


class RotateCommand(BaseClass):
    """
    A class to issue a remote 
    """
    def __init__(self, connection, retries=2):
        """
        :param:

         - `connection`: A connection to the controller of the rate-table (rotator)
         - `retries`: The number of times to retry
        """
        super(RotateCommand, self).__init__()
        self.connection = connection
        self.retries = retries
        return

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: namedtuple with parameters.angle_velocity.parameters
        """
        angle, velocity = parameters.angle_velocity.parameters
        arguments = "{0} --velocity {1}".format(angle, velocity)
        stdout, stderr = self.connection.rotate(arguments)
        try:
            timeout = parameters.timeout
        except AttributeError:
            self.logger.debug("Using default 2 minute timeout")
            timeout = 120
        end_time = time.time() + 120
        
        for line in stdout:
            if 'Setting the table angle' in line:
                self.logger.info(line)
            elif 'Table Angle:' in line:
                self.logger.info(line)
            else:                
                self.logger.debug(line)
            if time.time() > end_time:
                self.kill()
                raise RotateError("Rotation exceeded timeout ({0})".format(timeout))
        for line in stderr:
            if len(line) > 1:
                self.logger.error(line)
            if "Requested position is out of range." in line:
                raise ConfigurationError("Requested rotation angle of {0} is out of range".format(parameters.angles.parameters))
        return "angle_{0}".format(angle.zfill(3))

    def check_errors(self, line):
        """
        :param:

         - `line`: line of output from the rotate command

        :raise: CommandError if a known fatal error is detected
        """
        if "No such file or directory" in line:
            raise CommandError("The Rotator was not found -- is the USB cable plugged in?")
        return

    def kill(self):
        """
        :postcondition: rotate process killed
        """
        kill = KillAll(name='rotate')
        kill(self.connection)
        return
# end class RotateCommand


if __name__ == "__main__":
    import time
    from apetools.connections.sshconnection import SSHConnection
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
