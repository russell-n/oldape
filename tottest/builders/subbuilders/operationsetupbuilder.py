"""
A module to build operation setups
"""
from basetoolbuilder import BaseToolBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.operationsetup import DummySetupOperation
from tottest.commons.errors import ConfigurationError

class OperationSetupBuilder(BaseToolBuilder):
    """
    A class to build Setup Operations
    """
    def __init__(self, *args, **kwargs):
        super(OperationSetupBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def product(self):
        """
        :return: Operation Setup object
        
        """
        if self._product is None:
            try:
                tools = self.config_map.get_list(ConfigOptions.test_section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummySetupOperation()
        return self._product

    @property
    def parameters(self):
        return self._parameters
# end class SetupOperationBuilder
