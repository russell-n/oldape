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
    def section(self):
        """
        :return: the name of the section in the config file
        """
        if self._section is None:
            self._section = ConfigOptions.test_section
        return self._section 
    
    @property
    def product(self):
        """
        :return: Operation Setup object
        
        """
        if self._product is None:
            try:
                tools = self.config_map.get_list(self.section,
                                                 ConfigOptions.operation_setup_option,)
            except ConfigurationError as error:
                self.logger.debug(error)                
                self._product = DummySetupOperation()
        return self._product

    @property
    def parameters(self):
        return self._parameters
# end class SetupOperationBuilder
