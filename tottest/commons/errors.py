"""
A module to hold common exceptions
"""

class ConnectionError(Exception):
    """
    A ConnectionError is raised by connectinos to indicate a problem.
    """
    pass
# end class ConnectionError

class ConnectionWarning(Exception):
    """
    A connection warning is a non-fatal connection-related error.
    """
    pass
# end class ConnectionWarning

class TimeoutError(Exception):
    """
    A TimeoutError is a generic Timeout exception to wrap the various timeout
    """
    pass
# end class TimeoutError

class CommandError(Exception):
    """
    A CommandError reflects a problem with the command on the Device-side
    """
    pass
# end class CommandError

class ConfigurationError(Exception):
    """
    A ConfigurationError is raised if there is an error in the configuration file
    """
    pass
# end class ConfigurationError

class StorageError(Exception):
    """
    An StoragError is raised by the StorageOutput
    """
    pass
# end class StorageError
    
class AffectorError(Exception):
    """
    An Affector Error is raised for non-recoverable affector errors
    """
# end class AffectorError

class ArgumentError(Exception):
    """
    raised if command-line arguments don't produce valid output
    """
# end class InvocationError
