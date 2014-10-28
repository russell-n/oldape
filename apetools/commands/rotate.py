
#python standard library
import time

# apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commons.errors import CommandError
from apetools.tools.killall import KillAll, KillAllError


SIGKILL = 9
PROCESS = 'rotate'


class RotateError(CommandError):
    """
    An error in the rotation
    """
# end class RotateError


class RotateParameters(object):
    """
    RotateParameters for the rotate command
    """
    def __init__(self, angles, configuration=None, section=None, velocity=None,
                 acceleration=None, deceleration=None):
        """
        RotateParameters constructor

        :param:

         - `angles`: iterable collection of angles
         - `configuration`: path to configuration file
         - `section`: section header in configuration file
         - `velocity`: rate at which to rotate
         - `acceleration`: rate at which to accelerate
         - `deceleration`: rate at which to decelerate
        """
        self.angles = angles
        self._configuration = ""
        self.configuration = configuration
        self._non_angle_arguments = None
        self._section = ""
        self.section = section
        self._velocity = ""
        self.velocity = velocity
        self._acceleration = ""
        self.acceleration = acceleration
        self._deceleration = ""
        self.deceleration = deceleration       
        return

    @property
    def deceleration(self):
        """
        deceleration option
        """
        return self._deceleration

    @deceleration.setter
    def deceleration(self, deceleration):
        """
        sets the deceleration option

        :param:

         - `deceleration`: value for the deceleration option
        """
        if deceleration is not None:
            self._deceleration = " --deceleration {0}".format(deceleration)
        return

    @property
    def acceleration(self):
        """
        acceleration option
        """
        return self._acceleration

    @acceleration.setter
    def acceleration(self, acceleration):
        """
        Sets the acceleration option
        """
        if acceleration is not None:
            self._acceleration = " --acceleration {0}".format(acceleration)
        return self._acceleration

    @property
    def velocity(self):
        """
        Velocity option
        """
        return self._velocity

    @velocity.setter
    def velocity(self, velocity):
        """
        Sets the velocity option

        :param:

         - `velocity`: rate for the table
        """
        if velocity is not None:
            self._velocity = " --velocity {0}".format(velocity)
        return

    @property
    def section(self):
        """
        Configuration section option
        """
        return self._section

    @section.setter
    def section(self, section):
        """
        sets the section option

        :param:

         - `section`: name of section in the configuration
        """
        if section is not None:
            self._section = " --section {0}".format(section)
        return

    @property
    def non_angle_arguments(self):
        """
        :return: argument string without angle
        """
        if self._non_angle_arguments is None:
            self._non_angle_arguments = "".join([self.configuration,
                                                 self.section,
                                                 self.velocity,
                                                 self.acceleration,
                                                 self.deceleration])
        return self._non_angle_arguments

    @property
    def configuration(self):
        """
        The configuration argument
        """
        return self._configuration

    @configuration.setter
    def configuration(self, configuration):
        """
        Sets the configuration option

        :param:

         - `configuration`: path to configuration or None

        :postcondition: self._configuration is set
        """
        if configuration is not None:
            self._configuration = " --configuration {0}".format(configuration)
        return
        
    @property
    def arguments(self):
        """
        Generator of arguments for the rotate command
        """
        for angle in self.angles:
            yield "{0} {1}".format(self.non_angle_arguments,
                                   angle)


class RotateCommand(BaseClass):
    """
    A class to issue a remote 'rotate' command
    """
    def __init__(self, connections, retries=2):
        """
        :param:

         - `connections`: list of connections to turntable controls
         - `retries`: The number of times to retry
        """
        super(RotateCommand, self).__init__()
        self.connections = connections
        self.retries = retries
        self._killers = None
        return

    @property
    def killers(self):
        """
        :return: rotate process killer
        """
        if self._killers is None:            
            self._killers = [KillAll(connection=connection,
                                 name=PROCESS) for connection in self.connections]
        return self._killers


    def kill_process(self):
        """
        Kills rotate processes over the connection

         * If the default level fails, tries a -9

        """
        self.logger.info('Killing any existing rotate processes')
        for kill in self.killers:
            try:
                kill()
            except KillAllError as error:
                self.logger.warning(error)
                kill.level = SIGKILL
                kill()            
        return
    
    def rotate(self, connection, arguments, timeout=120):
        """
        sends the arguments to the connection
        """
        stdout, stderr = connection.rotate(arguments, timeout=4)
        end_time = time.time() + timeout
        eof = True
        for line in stdout:
            self.logger.debug("rotate stdout: {0}".format(line))
            if 'Setting the table angle' in line:
                self.logger.info(line)
            elif 'Table Angle:' in line:
                self.logger.info(line.rstrip())
            elif 'Rotate Main Ending' in line:
                self.logger.debug("End of program detected, no end of file reached.")
                eof = False
                break
            else:
                self.logger.debug(line)
            if time.time() > end_time:
                message = "Rotation exceeded timeout ({0})"
                self.kill_process()
                raise RotateError(message.format(timeout))
        self.logger.debug("Finished with rotation Standard out.")
        if not eof:
            self.logger.debug("Checking rotation Standard error")
            # the stderr isn't getting closed sometimes
            # don't iterate over it
            line =  stderr.readline(timeout=1)
            if len(line) > 1:
                self.logger.error(line)
                if "Requested position is out of range." in line:
                    angle = parameters.angles.parameters
                    message = "Angle out of range: {0}".format(angle)
                    raise ConfigurationError(message)
        return
    
    def __call__(self, parameters, filename_prefix=None):
        """
        :param:

         - `parameters`: namedtuple with parameters.angle_velocity.parameters
         - `filename_prefix`: not used
        """
        self.kill_process()
        angle, velocity, clockwise = parameters.angle_velocity.parameters
        arguments = "{0} --velocity {1}".format(angle, velocity)
        if clockwise:
            arguments += " --clockwise"
        try:
            timeout = parameters.timeout
        except AttributeError:
            self.logger.debug("Using default 2 minute timeout")
            timeout = 120

        for connection in self.connections:
            self.logger.info("Rotating: {0}".format(arguments))
            self.rotate(connection, arguments, timeout)
        return "angle_{0}".format(angle.zfill(3))

    def check_errors(self, line):
        """
        :param:

         - `line`: line of output from the rotate command

        :raise: CommandError if a known fatal error is detected
        """
        if "No such file or directory" in line:
            message = "Rotator not found -- USB cable plugged in?"
            raise CommandError(message)
        return

# end class RotateCommand


if __name__ == "__main__":
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
