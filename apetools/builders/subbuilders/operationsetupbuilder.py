
from baseoperationbuilder import BaseOperationBuilder
from apetools.lexicographers.config_options import ConfigOptions
from apetools.operations.operationsetup import OperationSetup


class OperationSetupBuilder(BaseOperationBuilder):
    """
    A class to build Operation Setups
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: Builder (inherited argument)
         - `config_map`: ConfigurationMap (inherited argument)
        """
        super(OperationSetupBuilder, self).__init__(*args, **kwargs)
        return

    @property
    def config_option(self):
        """
        :return: config_file option for this operation
        """
        if self._config_option is None:
            self._config_option = ConfigOptions.operation_setup_option
        return self._config_option

    @property
    def operation(self):
        """
        :return: the class definition for this operation
        """
        if self._operation is None:
            self._operation = OperationSetup
        return self._operation

    @property
    def section(self):
        """
        :return: None
        """
        return self._section
# end class SetupOperationBuilder
