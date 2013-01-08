
from apetools.commons.errors import ConfigurationError
from pollerbuilders import BasePollerBuilder
from apetools.watchers.fileexpressionwatcher import BatteryWatcher


class BatteryWatcherBuilder(BasePollerBuilder):
    """
    A class to build a battery-status watcher
    """
    def __init__(self, *args, **kwargs):
        super(BatteryWatcherBuilder, self).__init__(*args, **kwargs)
        self._name = None
        return

    @property
    def name(self):
        """
        :return: the path to the proc-file
        """
        if self._name is None:
            try:
                self._name = self.parameters.name
            except AttributeError as error:
                self.logger.error(error)
                raise ConfigurationError("name (of the source file) is a required parameter for the BatteryWatcher")
        return self._name

    @property
    def product(self):
        """
        :return: a built battery-watcher
        """
        if self._product is None:
            use_header = self.use_header
            self._product = BatteryWatcher(device=self.node,
                                           output=self.output_file,
                                           interval=self.interval,
                                           name=self.name,
                                           use_header=use_header)
        return self._product       
# end class BatteryWatcherBuilder
