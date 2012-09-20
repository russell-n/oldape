"""
A module to build test teardowns
"""

from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.teardowntest import DummyTeardownTest
from tottest.commons.errors import ConfigurationError

class TeardownTestBuilder(BaseClass):
    """
    A class to build Setup Operations
    """
    def __init__(self, config_map):
        super(TeardownTestBuilder, self).__init__()
        self.config_map = config_map
        self._teardown_test = None
        return

    @property
    def teardown_test(self):
        """
        :return: Teardown Test object
        
        """
        if self._teardown_test is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._teardown_test = DummyTeardownTest()
        return self._teardown_test
# end class TeardownTestBuilder
