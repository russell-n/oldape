"""
A module to build test teardowns
"""

from baseoperationbuilder import BaseOperationBuilder
from apetools.lexicographers.config_options import ConfigOptions
from apetools.operations.teardowntest import TeardownTest
from apetools.commons.errors import ConfigurationError

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
            self._operation = TeardownTest
        return self._operation

    @property
    def section(self):
        """
        :return: None
        """
        return self._section
# end class TeardownTestBuilder
