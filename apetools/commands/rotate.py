
#python standard library
import time

# apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError
from apetools.commons.errors import CommandError
from apetools.tools.killall import KillAll, KillAllError
from apetools.commands.rotation_arguments import BaseArguments

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
    def __init__(self, configuration, section):
        """
        RotateParameters constructor

        :param:

         - `configuration`: Configuration Map with settings
         - `section`: section header in configuration file
        """
        self.configuration = configuration
        self.section = section
        self._angles = None
        self._argument_strings = None
        self._values_string = None
        self._booleans_string = None
        self._base_arguments = None        
        return

    @property
    def base_arguments(self):
        """
        A Rotate BaseArguments object 
        """
        if self._base_arguments is None:
            self._base_arguments = BaseArguments(args=[])
        return self._base_arguments

    @property
    def values_string(self):
        """
        :return: string of options with values
        """
        if self._values_string is None:
            self._values_string = ''.join([" --{0} {1}".format(option,
                                                               self.configuration.get(section=self.section,
                                                                  option=option,
                                                                  optional=True))
                                                                  for option in self.base_arguments.value_options
                                                                  if self.configuration.get(section=self.section,
                                                                                            option=option,
                                                                                            optional=True) is not None])
        return self._values_string

    @property
    def booleans_string(self):
        """
        :return: string of boolean options 
        """
        if self._booleans_string is None:
            self._booleans_string = ''.join([" --{0}".format(option)
                                            for option in self.base_arguments.boolean_options
                                            if self.configuration.get_boolean(section=self.section,
                                                                                option=option,
                                                                                optional=True,
                                                                                default=False)])
        return self._booleans_string

    @property
    def angles(self):
        """
        List of angles from the configuration
        """
        if self._angles is None:
            self._angles = self.configuration.get_ints(section=self.section,
                                                       option='angles')
        return self._angles

    @property
    def argument_strings(self):
        """
        Generates argument strings for each angle
        """
        for angle in self.angles:
            yield "{0}{1} {2}".format(self.booleans_string,
                                        self.values_string,
                                        angle)

class RotateCommand(BaseClass):
    """
    A class to issue a remote 'rotate' command (older version for pre-Cameron turntables)
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

        :param:

         - `connection`: connection to the turntable controller
         - `arguments`: string of arguments for rotate command
         - `timeout`: time to wait for the table to finish

        :raise: ConfigurationError if table complains about arguments
        :raise: RotateError if timeout reached before table finishes
        """
        # the timeout here is an SSH timeout (or other connection timeout)
        # not the timeout waiting for the table to finish
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

class RotateCommandUsurper(RotateCommand):
    """
    Command to rotate turntables
    """
    def __call__(self, parameters, filename_prefix=None):
        """
        Main interface to rotate tables

        :param:

         - `parameters`: object with turntable.parameters attribute
         - `filename_prefix`: Not used
        """
        self.kill_process()
        output_string = ""
        
        for connection in self.connections:
            arguments = parameters.turntable.parameters[connection.identifier]
            output_string += "{0}_{1}".format(connection.identifier,
                                              "_".join(arguments.replace('-', '').split()))

            self.rotate(connection=connection,
                        arguments=arguments)
        return output_string

    def rotate(self, connection, arguments='', timeout=600):
        """
        Assumes that the command will block until done and nothing unusual happens

        :param:

         - `connection`: connection to the table (ssh)
         - `arguments`: string to pass to the command
        """
        stdout, stderr = connection.rotate(arguments,
                                           timeout)
        
        for line in stdout:
            self.logger.info(line)

        for line in stderr:
            self.log_error(line)
        return

if __name__ == "__main__":
    from apetools.connections.sshconnection import SSHConnection
    c = SSHConnection("pogo2", "root")
    r = RotateCommand(c)
    print("Rotate to 90 degrees")
    r(90)
    time.sleep(1)
    print("Rotate to 180 Degrees")
    r(180)
    time.sleep(1)
    print( "Rotate to 0 degrees")
    r()