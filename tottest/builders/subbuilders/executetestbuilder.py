"""
A module to build tests
"""

from basetoolbuilder import BaseToolBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.executetest import DummyExecuteTest
from tottest.commons.errors import ConfigurationError

class ExecuteTestBuilder(BaseToolBuilder):
    """
    A class to build Setup Operations
    """
    def __init__(self, *args, **kwargs):
        super(ExecuteTestBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: Execute Test object
        
        """
        if self._product is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummyExecuteTest()
        return self._product

    @property
    def parameters(self):
        """
        :return:
        """
        if self._parameters is None:
            self._parameters = []
        return self._parameters
# end class ExecuteTestBuilder
