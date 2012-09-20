"""
A module to build operation teardowns
"""

from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.operationteardown import DummyTeardownOperation
from tottest.commons.errors import ConfigurationError

class OperationTeardownBuilder(BaseClass):
    """
    A class to build Teardown Operations
    """
    def __init__(self, config_map):
        super(OperationTeardownBuilder, self).__init__()
        self.config_map = config_map
        self._operation_teardown = None
        return

    @property
    def operation_teardown(self):
        """
        :return: Operation Teardown object
        
        """
        if self._operation_teardown is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_teardown_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._operation_teardown = DummyTeardownOperation()
        return self._operation_teardown
# end class TeardownOperationBuilder
