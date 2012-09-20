"""
A module to build tests
"""

from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.executetest import DummyExecuteTest
from tottest.commons.errors import ConfigurationError

class ExecuteTestBuilder(BaseClass):
    """
    A class to build Setup Operations
    """
    def __init__(self, config_map):
        super(ExecuteTestBuilder, self).__init__()
        self.config_map = config_map
        self._execute_test = None
        return

    @property
    def execute_test(self):
        """
        :return: Execute Test object
        
        """
        if self._execute_test is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._execute_test = DummyExecuteTest()
        return self._execute_test
# end class ExecuteTestBuilder
