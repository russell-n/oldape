"""
A module to build test teardowns
"""

from baseoperationbuilder import BaseOperationBuilder
from tottest.lexicographers.config_options import ConfigOptions
from tottest.operations.teardowntest import DummyTeardownTest
from tottest.commons.errors import ConfigurationError

class TeardownTestBuilder(BaseOperationBuilder):
    """
    A class to build Setup Operations
    """
    def __init__(self, *args, **kwargs):
        super(TeardownTestBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def config_option(self):
        """
        :return: the name of the option for this builder in config file
        """
        if self._config_option is None:
            self._config_option = ConfigOptions.teardown_test_option
        return self._config_option

    @property
    def operation(self):
        """
        :return: the class for to build
        """
        if self._operation is None:
            self._operation = DummyTeardownTest
        return self._operation
# end class TeardownTestBuilder
