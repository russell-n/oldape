
"""rotate (a turntable controller)

Usage: rotate -h | -v
       rotate [options] <angle>
       
Help Options:

    -h, --help     Display this help message and quit.
    -v, --version  Display the version number and quit.

Configuration File:

    --configuration=<path>  Path to (optional) configuration file.
    --section=<section>     Section name in configuration file [default: rotator]

Logging Options:

    --debug   Set logging level to DEBUG.
    --silent  Set logging level to ERROR.

Debugging Options:

    --pudb       Enable the `pudb` debugger (if installed)
    --pdb        Enable the `pdb` (python's default) debugger

Orientation Options:

    -k --clockwise     Rotate clockwise instead of anti-clockwise

Test Options:

    --test   Use a Mock Rotator to check the arguments
    --crash  Make the MockRotator raise an exception

Rotation Arguments:

    -r, --velocity=<rate>           Rate at which to rotate (from 1.512 to 720) [default: 50].
    -a, --acceleration=<accel>      Rate at which to accelerate to velocity (0.167 to 5461.167) [default: 100].
    -d, --deceleration=<decel>      Rate at which to decelerate to stop (0.167 to 5461.167) [default: 100].
    -t, --timeout=<seconds>         Time to wait for table to reach target angle [default: 10]
    <angle>                         Angle to rotate table to (0 to 359) [default: 0].

Set Table Angle:
    The table doesn't have a sensor to tell it where it's at when it's turned on.
    Whenever it is powered up, you should tell it what angle it's at.

    --set  If set, calls set_angle instead of rotate function
"""

# python standard library
from argparse import ArgumentParser
import os

# third-party
from schema import Schema, Or, And, Use, SchemaError

# this package
from apetools import VERSION, BaseClass

DEGREES_IN_CIRCLE = 360

# from ht.cfg [rotator]
MIN_ACCELERATION = 0.167
MAX_ACCELERATION = 5461.167

# calculated from the ht.cfg velocity range
MIN_VELOCITY = 1.512
MAX_VELOCITY = 720

class ArgumentsConstants(object):
    """
    Constants for the arguments
    """
    __slots__ = ()
    #options
    acceleration = "--acceleration"    
    angle = "<angle>"
    clockwise = "--clockwise"
    configuration = '--configuration'
    crash = '--crash'
    debug = "--debug"
    deceleration = '--deceleration'
    pdb = '--pdb'
    pudb = "--pudb"
    section = '--section'
    set_option = '--set'
    silent = '--silent'
    velocity = '--velocity'
    timeout = '--timeout'

    #defaults
    default_configuration = "rotator.ini"
    default_angle = 0
    default_section = 'rotator'
    default_velocity = 50
    default_timeout = 10
    default_acceleration = 100
    default_deceleration = 100
# end ArgumentConstants

args_schema = {}

acceleration = ArgumentsConstants.acceleration
args_schema[acceleration] = Schema(And(Use(float, error='acceleration must be float'),
                                       lambda a: MIN_ACCELERATION <= a <= MAX_ACCELERATION,
                                       error=("acceleration out of range: "
                                              "({0} <= accel <= {1})").format(MIN_ACCELERATION,
                                                                              MAX_ACCELERATION)))

deceleration = ArgumentsConstants.deceleration
args_schema[deceleration] = Schema(And(Use(float, error='deceleration must be float'),
                                       lambda a: MIN_ACCELERATION <= a <= MAX_ACCELERATION,
                                       error=("deceleration out of range: "
                                              "({0} <= accel <= {1})").format(MIN_ACCELERATION,
                                                                              MAX_ACCELERATION)))

angle = ArgumentsConstants.angle
args_schema[angle] = Schema(And(Use(int,
                                    error='Angle must be an integer'),
                                Use(lambda a: a % DEGREES_IN_CIRCLE)))

if __name__ == '__builtin__':
    print( ".. csv-table:: Modulo Example")
    print( "   :header: Angle, Angle % 360\n")
    for angle in xrange(0, -360, -45):
        print( "   {0},{1}".format(angle, angle % 360))

velocity = ArgumentsConstants.velocity
args_schema[velocity] = Schema(And(Use(float,
                                       error="'velocity' must be a real number"),
                                        lambda v: MIN_VELOCITY <= v <= MAX_VELOCITY,
                                        error="velocity out of range ({0} <= v < {1})".format(MIN_VELOCITY,
                                                                                             MAX_VELOCITY )))

config = ArgumentsConstants.configuration
args_schema[config] = Schema(Or(None,
                                lambda c: os.path.isfile(c),
                                error="File not found"))

timeout = ArgumentsConstants.timeout
args_schema[timeout] = Schema(And(Use(float),
                                  lambda t: t >= 0,
                                  error='timeout must be a non-negative float'))

class ArgumentError(SchemaError):
    """
    Error to raise if the schema validation fails
    """

class BaseArguments(BaseClass):
    def __init__(self, args=None):
        """
        BaseArguments constructor

        :param:

         - `args`: list of arguments for ArgumentParser
        """
        super(BaseArguments, self).__init__()
        self._parser = None
        self._logger = None
        self.args = args
        self._debug = None
        self._silent = None
        self._arguments = None
        self._pudb = None
        self._pdb = None
        self._configuration = None
        self._angle = None
        self._section = None
        self._velocity = None
        self._set = None
        self._clockwise = None
        self._acceleration = None
        self._deceleration = None
        self._timeout = None
        self._test = None
        self._crash = None
        self._options = None
        self._boolean_options = None
        self._value_options = None
        return

    @property
    def value_options(self):
        """
        :return: list of value-option names
        """
        if self._value_options is None:
            self._value_options = [option for option in self.options
                                   if option not in self.boolean_options]
        return self._value_options                                   

    @property
    def boolean_options(self):
        """
        :return: List of boolean-option names
        """
        if self._boolean_options is None:
            self._boolean_options = [option for option in self.options
                                     if (getattr(self.arguments, option) is True or
                                         getattr(self.arguments, option) is False)]
        return self._boolean_options                                         

    @property
    def options(self):
        """
        :return: list of options
        """
        if self._options is None:
            self._options = vars(self.arguments).keys()
        return self._options

    @property
    def crash(self):
        """
        :return: --crash option
        :rtype: boolean
        """
        if self._crash is None:
            self._crash = self.arguments.crash
        return self._crash

    @property
    def test(self):
        """
        :return: --test option
        :rtype: bool
        """
        if self._test is None:
            self._test = self.arguments.test
        return self._test

    @property
    def timeout(self):
        """
        The time (seconds) to wait for the table to reach position

        :rtype: float
        :return: argument for Rotator.waitForPosition
        """
        if self._timeout is None:
            validate = args_schema[ArgumentsConstants.timeout].validate
            try:
                self._timeout = validate(self.arguments.timeout)
            except SchemaError as error:
                self.log_error(error)
                raise ArgumentError(autos=None,
                                    errors="Invalid Timeout: '{0}'".format(self.arguments.timeout))
        return self._timeout

    @property
    def parser(self):
        """
        ArgParse argument parser
        """
        if self._parser is None:
            self._parser = ArgumentParser(description='A turntable control',
                                          version=VERSION)
            log_group = self._parser.add_mutually_exclusive_group()
            log_group.add_argument("--debug", action='store_true',
                                   default=False, help='Change logging to DEBUG level (noisier).')
            log_group.add_argument("--silent", action='store_true',
                                   default=False, help="Change logging to ERROR level (quieter).")

            debugger_group = self._parser.add_mutually_exclusive_group()
            debugger_group.add_argument('--pudb', action='store_true',
                                        default=False, help='Enable pudb debugger')
            debugger_group.add_argument('--pdb', action='store_true', default=False,
                                        help='Enable pdb debugger')

            self._parser.add_argument('--configuration', help='Path to configuration file to override table defaults')
            self._parser.add_argument('--section', default='rotator',
                                      help='Section name within config file with values (default=%(default)s)')
                                      
            self._parser.add_argument('-r', '--velocity', default=ArgumentsConstants.default_velocity, type=float,
                                      help='velocity (rate) at which to spin table (1.512 to 720 deg/second) (default=%(default)s)')
                                      
            self._parser.add_argument('-a', '--acceleration', default=ArgumentsConstants.default_acceleration, type=float,
                                      help='Rate at which to speed up to velocity (0.167 to 5,461.176).')
            self._parser.add_argument('-d', '--deceleration', default=ArgumentsConstants.default_deceleration, type=float,
                                      
                                      help='Rate at which to slow down to 0 (0.167 to 5,461.176).')
            self._parser.add_argument('-k', '--clockwise',
                                      help='spin clockwise instead of anti-clockwise (the default)',
                                      action='store_true', default=False)
            self._parser.add_argument("angle", default=ArgumentsConstants.default_angle,
                                      type=int, nargs='?',
                                      help='Angle to rotate to in degrees (default=%(default)s)')

            self._parser.add_argument('--set', action='store_true',
                                      default=False,
                                      help="Tell the table its current angle instead of rotating (to zero it out when it's turned on).")
            self._parser.add_argument("-t", '--timeout', default=ArgumentsConstants.default_timeout,
                                      type=float, help="Seconds to wait for table to reach position (default=%(default)s)")
            self._parser.add_argument('--test', action='store_true', default=False,
                                      help="Use Mock Rotator to test the configuration")
            self._parser.add_argument('--crash', action='store_true', default=False,
                                      help='Tell the MockRotator to raise an Exception')
        return self._parser
        
    @property
    def deceleration(self):
        """
        The turntable's deceleration

        :return: steps/second/second (default None)
        """
        if self._deceleration is None:
            validate = args_schema[ArgumentsConstants.deceleration].validate
            try:
                self._deceleration = validate(self.arguments.deceleration)
            except SchemaError as error:
                self.log_error(error)
                raise ArgumentError(autos=None,
                                    errors="Invalid Deceleration: '{0}'".format(self.arguments.deceleration))
        return self._deceleration

    @property
    def acceleration(self):
        """
        The turntable acceleration

        :return: steps/second/second (default None)
        """
        if self._acceleration is None:
            validate = args_schema[ArgumentsConstants.acceleration].validate
            try:
                self._acceleration = validate(self.arguments.acceleration)
            except SchemaError as error:
                self.log_error(error)
                raise ArgumentError(errors="Invalid Acceleration: '{0}'".format(self.arguments.acceleration),
                                    autos=None)
                
        return self._acceleration

    @property
    def angle(self):
        """
        The angle to rotate to (converts to anticlockwise if --clockwise not set)
        """
        if self._angle is None:
            validate = args_schema[ArgumentsConstants.angle].validate
            self._angle = validate(self.arguments.angle)
            self._angle = self.adjust_angle(self._angle)
        return self._angle

    @property
    def clockwise(self):
        """
        Flag to indicate clockwise rotation instead of anti-clockwise
        """
        if self._clockwise is None:
            self._clockwise = self.arguments.clockwise
        return self._clockwise

    @property
    def set(self):
        """
        if true, set the table's current angle instead of rotating
        """
        if self._set is None:
            self._set = self.arguments.set
        return self._set

    @property
    def velocity(self):
        """
        The rate at which to spin (from 20 to 720 Degrees/Revolution)
        """
        if self._velocity is None:
            try:
                validate = args_schema[ArgumentsConstants.velocity].validate
                self._velocity = validate(self.arguments.velocity)
            except SchemaError as error:
                self.log_error(error)
                raise ArgumentError(errors="Invalid Velocity: '{0}'".format(self.arguments.velocity),
                                    autos=None)
                raise
        return self._velocity

    @property
    def section(self):
        """
        The configuration section name with rotator settings
        """
        if self._section is None:
            self._section = self.arguments.section
        return self._section    

    def adjust_angle(self, angle):
        """
        Checks if the 'clockwise' flag set, converts to anticlockwise if not

        :param:

         - `angle`: angle in degrees to convert (if needed)

        :return: angle
        :rtype: IntegerType
        :raise: TypeError if angle can't be cast to an integer
        """
        # the previous turntable used anti-clockwise rotation
        # and Henry asked that this be made the default
        # so this will only turn clockwise if explicitly asked
        if not self.clockwise:
            # if angle is 0 it needs to be modded to avoid 360
            angle = (DEGREES_IN_CIRCLE - angle) % DEGREES_IN_CIRCLE
        return angle
        
    @property
    def configuration(self):
        """
        Path to the configuration file
        """
        if self._configuration is None:
            validate = args_schema[ArgumentsConstants.configuration].validate
            try:
                self._configuration = validate(self.arguments.configuration)
            except SchemaError as error:
                self.log_error(error)
                raise ArgumentError(autos=None,
                                    errors="Invalid Configuration File Path: '{0}'".format(self.arguments.configuration))
            if self._configuration is None:
                # use the file in this package
                module = __import__('rotation_table')
                path_to_module = module.__path__[0]
                self._configuration = os.path.join(path_to_module,
                                                   ArgumentsConstants.default_configuration)
        return self._configuration
        
    @property
    def arguments(self):
        """
        Namespace of parsed arguments
        """
        if self._arguments is None:
            self._arguments = self.parser.parse_args(self.args)
        return self._arguments

    @property
    def debug(self):
        """
        Option to change logging level to debug

        :rtype: Boolean
        """
        if self._debug is None:
            self._debug = self.arguments.debug
        return self._debug

    @property
    def silent(self):
        """
        Option to change logging level to error
        :rtype: Boolean
        """
        if self._silent is None:
            self._silent = self.arguments.silent
        return self._silent

    @property
    def pudb(self):
        """
        Option to enable pudb debugger
        :rtype: Boolean
        """
        if self._pudb is None:
            self._pudb = self.arguments.pudb
        return self._pudb

    @property
    def pdb(self):
        """
        Option to enable the python debugger
        :rtype: Boolean
        """
        if self._pdb is None:
            self._pdb = self.arguments.pdb
        return self._pdb

    def reset(self):
        """
        resets the properties to None
        """
        self._arguments = None
        self._acceleration = None
        self._angle = None
        self._clockwise = None
        self._configuration = None
        self._debug = None
        self._deceleration = None
        self._pdb = None
        self._pudb = None
        self._section = None
        self._set = None
        self._silent = None
        self._timeout = None
        self._velocity = None
        return

    def check_rep(self):
        """
        tries to get all the parameters (relies on the validators)
        """
        attributes= ("acceleration angle clockwise configuration"
                     " debug deceleration pdb pudb section set "
                     "silent timeout velocity").split()
        for attribute in attributes:
            getattr(self, attribute)
# end class BaseArguments