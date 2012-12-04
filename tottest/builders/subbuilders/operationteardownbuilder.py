"""
A module to build operation teardowns
"""

from basetoolbuilder import BaseToolBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.operationteardown import DummyTeardownOperation
from tottest.commons.errors import ConfigurationError

class OperationTeardownBuilder(BaseToolBuilder):
    """
    A class to build Teardown Operations
    """
    def __init__(self, *args, **kwargs):
        super(OperationTeardownBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: Operation Teardown object
        
        """
        if self._product is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_teardown_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummyTeardownOperation()
        return self._product

    @property
    def parameters(self):
        """
        :return: list of namedtuples
        """
        if self._parameters is None:
            self._parameters = self.previous_parameters
        return self._parameters
# end class TeardownOperationBuilder
