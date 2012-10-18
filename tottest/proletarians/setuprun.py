"""
A module to hold the SetUp
"""

# tottest Libraries
from tottest.baseclass import BaseClass
from tottest.builders import builder
from tottest.lexicographers.lexicographer import Lexicographer

class SetUp(BaseClass):
    """
    The SetUp sets up the infrastructure
    """
    def __init__(self, arguments, *args, **kwargs):
        """
        :param:

         - `arguments`: An ArgumentParser Namespace
        """
        super(SetUp, self).__init__(*args, **kwargs)
        self.arguments = arguments
        self._lexicographer = None
        self._builder = None
        return

    @property
    def lexicographer(self):
        """
        :return: Lexicographer that maps config-files
        """
        if self._lexicographer is None:
            glob = self.arguments.glob
            message = "Building Lexicographer with glob ({0})".format(glob)
            self.logger.debug(message)
            self._lexicographer = Lexicographer(glob)
        return self._lexicographer

    @property
    def builder(self):
        """
        :return: A builder of objects
        """
        if self._builder is None:
            l = self.lexicographer
            message = "Building builder with Lexicographer '{0}'".format(str(l))
            self.logger.debug(message)
            self._builder = builder.Builder(l)
        return self._builder
        
    def __call__(self):
        """
        Runs the builder.hortator's `run` method    
        """
        self.logger.debug("Calling the hortator's run.")
        self.builder.hortator()
        return            
# end SetUp
