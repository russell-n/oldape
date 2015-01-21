
from baseoperationbuilder import BaseOperationBuilder
from apetools.lexicographers.config_options import ConfigOptions
from apetools.operations.operationteardown import OperationTeardown


class OperationTeardownBuilder(BaseOperationBuilder):
    """
    A class to build Teardown Operations
    """
    def __init__(self, *args, **kwargs):
        super(OperationTeardownBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def config_option(self):
        """
        Name of the option expected in the config-file
        """
        if self._config_option is None:
            self._config_option = ConfigOptions.operation_teardown_option
        return self._config_option

    @property
    def operation(self):
        """
        :return: Operation Teardown object
        
        """
        if self._operation is None:
            self._operation = OperationTeardown
        return self._operation

    @property
    def section(self):
        """
        Section name expected in the config-file
        """
        return self._section
# end class TeardownOperationBuilder
