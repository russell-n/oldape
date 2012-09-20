"""
A module to build operation setups
"""

from tottest.baseclass import BaseClass
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.operationsetup import DummySetupOperation
from tottest.commons.errors import ConfigurationError

class OperationSetupBuilder(BaseClass):
    """
    A class to build Setup Operations
    """
    def __init__(self, config_map):
        super(OperationSetupBuilder, self).__init__()
        self.config_map = config_map
        self._operation_setup = None
        return

    @property
    def operation_setup(self):
        """
        :return: Operation Setup object
        
        """
        if self._operation_setup is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._operation_setup = DummySetupOperation()
        return self._operation_setup
# end class SetupOperationBuilder
