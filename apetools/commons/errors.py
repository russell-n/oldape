"""
A module to hold common exceptions

These are made sub-classes of the OperatorError so that
the hortator can recover and move on to the next hortator.

Any exception raised that isn't a sub-class of the OperatorError is
unexpected and will crash the program (to make it obvious).
"""

from apetools.proletarians.errors import OperatorError


class ConnectionError(OperatorError):
    """
    A ConnectionError is raised by connectinos to indicate a problem.
    """
    pass
# end class ConnectionError

class ConnectionWarning(OperatorError):
    """
    A connection warning is a non-fatal connection-related error.
    """
    pass
# end class ConnectionWarning

class TimeoutError(OperatorError):
    """
    A TimeoutError is a generic Timeout exception to wrap the various timeout
    """
    pass
# end class TimeoutError

class CommandError(OperatorError):
    """
    A CommandError reflects a problem with the command on the Device-side
    """
    pass
# end class CommandError

class ConfigurationError(OperatorError):
    """
    A ConfigurationError is raised if there is an error in the configuration file
    """
    pass
# end class ConfigurationError

class StorageError(OperatorError):
    """
    An StoragError is raised by the StorageOutput
    """
    pass
# end class StorageError
    
class AffectorError(OperatorError):
    """
    An Affector Error is raised for non-recoverable affector errors
    """
# end class AffectorError

class ArgumentError(OperatorError):
    """
    raised if command-line arguments don't produce valid output
    """
# end class InvocationError
