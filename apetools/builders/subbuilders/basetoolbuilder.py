"""
A base-class for tool-builders
"""
# python
from abc import ABCMeta, abstractproperty
from collections import namedtuple

# apetools
from apetools.baseclass import BaseClass
from apetools.commons.errors import ConfigurationError

class BaseToolBuilderError(ConfigurationError):
    """
    An error to raise if there's something wrong with the user's configuration
    """
# end class BaseToolBuilderError

    
Parameters = namedtuple("Parameters", "name parameters".split())


class BaseToolBuilder(BaseClass):
    """
    A Base class to build tool-builders around.
    """
    __metaclass__ =  ABCMeta
    def __init__(self, master, config_map, previous_parameters):
        """
        :param:

         - `master`: The master Builder (builder.py)
         - `config_map`: A populated configuration map
         - `previous_parameters`: A list of the parameters created by previous builders
        """
        super(BaseToolBuilder, self).__init__()
        self.master = master
        self.config_map = config_map
        self.previous_parameters = previous_parameters
        self._product = None
        self._parameters = None
        return

    @abstractproperty
    def product(self):
        """
        :return: the built tool-object
        """
        return self._product

    @abstractproperty
    def parameters(self):
        """
        :return: list of namedtuples - each needs a `name` property to identify it
        """
        if self._parameters is None:
            try:
                options = self.config_map.options(self.section)[0]
                self._parameters = self.config_map.get_namedtuple(self.section,
                                                                  options)
            except TypeError as error:
                raise BaseToolBuilderError(error)
        return self._parameters
# end class BaseToolBuilder
    
