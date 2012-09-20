"""
A module to build test setups
"""

from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.setuptest import DummySetupTest
from tottest.commons.errors import ConfigurationError

class SetupTestBuilder(BaseClass):
    """
    A class to build Test Setups
    """
    def __init__(self, config_map):
        super(SetupTestBuilder, self).__init__()
        self.config_map = config_map
        self._test_setup = None
        return

    @property
    def test_setup(self):
        """
        :return: Test Setup object
        
        """
        if self._test_setup is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.test_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._test_setup = DummySetupTest()
        return self._test_setup
# end class SetupTestBuilder
