"""
A parameter generator maps the lexicographer's static configuration to a set of test parameters

This way a config-file can declare a set: e.g. repetitions=10

and the parameter-generator will create 10 parameter-objects

"""

#python
from collections import namedtuple

# tottest
from tottest.baseclass import BaseClass
from tottest.commons import enumerations, errors
from parametertree import ParameterTree

AffectorTypes = enumerations.AffectorTypes
IperfDirection = enumerations.IperfDirection
ConfigurationError = errors.ConfigurationError

parameters = ("test_id repetition repetitions output_folder " +
              " receiver sender recovery_time affector").split()

class TestParameter(namedtuple('TestParameter', parameters)):
    """
    A TestParameter holds the settings for a single test-iteration
    """
    __slots__ = ()

    def __str__(self):
        return (self.__class__.__name__ + ":" +
                ','.join(("{f}:{v}".format(f=f, v=getattr(self,f))
                          for f in self._fields)))

    
# end class TestParameter

class ParameterGenerator(BaseClass):
    """
    A ParameterGenerator is an iterator that generates test-parameters.
    """
    def __init__(self, parameters, *args, **kwargs):
        """
        :param:

         - `parameters`: A list of parameter (namedtuple) lists
        """
        super(ParameterGenerator, self).__init__(*args, **kwargs)
        self.parameters = parameters
        self._tree = None
        return

    @property
    def tree(self):
        """
        :return: parameter-tree populated with parameters (possibly)
        """
        if self._tree is None:
            self._tree = ParameterTree(self.parameters)
        return self._tree


    def __iter__(self):
        """
        :yield: the next namedtuple of parameters
        """
        for parameters in self.tree.paths:
            yield parameters
        return
# end class ParameterGenerator
