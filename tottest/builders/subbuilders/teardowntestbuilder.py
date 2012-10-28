"""
A module to build test teardowns
"""

from basetoolbuilder import BaseToolBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.teardowntest import DummyTeardownTest
from tottest.commons.errors import ConfigurationError

class TeardownTestBuilder(BaseToolBuilder):
    """
    A class to build Setup Operations
    """
    def __init__(self, *args, **kwargs):
        super(TeardownTestBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: Teardown Test object
        
        """
        if self._product is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummyTeardownTest()
        return self._product

    @property
    def parameters(self):
        """
        """
        return self._parameters
# end class TeardownTestBuilder
