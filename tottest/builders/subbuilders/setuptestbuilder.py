"""
A module to build test setups
"""

from baseoperationbuilder import BaseOperationBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.setuptest import SetupTest

class SetupTestBuilder(BaseOperationBuilder):
    """
    A class to build Test Setups
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: Builder (inherited argument)
         - `config_map`: ConfigurationMap (inherited argument)
        """
        super(SetupTestBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def config_option(self):
        """
        :return: config_file option for this operation
        """
        if self._config_option is None:
            self._config_option = ConfigOptions.test_setup_option
        return self._config_option

    @property
    def operation(self):
        """
        :return: the class definition for this operation
        """
        if self._operation is None:
            self._operation = SetupTest
        return self._operation

    @property
    def section(self):
        """
        :return: None
        """
        return self._section
# end class SetupTestBuilder
