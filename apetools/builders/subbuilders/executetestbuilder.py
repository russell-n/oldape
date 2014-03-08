"""
A module to build tests
"""

from apetools.lexicographers.config_options import ConfigOptions
from apetools.operations.executetest import ExecuteTest 

from baseoperationbuilder import BaseOperationBuilder
 

class ExecuteTestBuilder(BaseOperationBuilder):
    """
    A class to build execute test Operations
    """
    def __init__(self, *args, **kwargs):
        super(ExecuteTestBuilder, self).__init__(*args, **kwargs)
        return
    

    @property
    def config_option(self):
        """
        :return: config-file option for this operation
        """
        if self._config_option is None:
            self._config_option = ConfigOptions.execute_test_option
        return self._config_option
    
    @property
    def operation(self):
        """
        :return: class definition for this operation
        """
        if self._operation is None:
            self._operation = ExecuteTest
        return self._operation
# end class ExecuteTestBuilder
