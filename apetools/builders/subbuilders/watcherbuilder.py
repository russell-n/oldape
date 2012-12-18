"""
A Watcher builder
"""

#apetools
from basetoolbuilder import BaseToolBuilder
from logwatcherbuilders import LogcatWatcherBuilder, LogWatcherBuilder
from pollerbuilders import RssiPollerBuilder, DevicePollerBuilder
from apetools.watchers import thewatcher

from apetools.lexicographers.config_options import ConfigOptions

class WatcherTypes(object):
    """
    The names of the valid watcher types
    """
    __slots__ = ()
    logcat = "logcat"
    adblogcat = 'adblogcat'
    rssi = "rssi"
    device = 'device'
# end class WatcherTypes

    
watcher_builder = {WatcherTypes.adblogcat:LogcatWatcherBuilder,
                   WatcherTypes.logcat:LogWatcherBuilder,
                   WatcherTypes.rssi:RssiPollerBuilder,
                   WatcherTypes.device:DevicePollerBuilder}

class WatcherBuilder(BaseToolBuilder):
    """
    builds a master logwatcher
    """
    def __init__(self, *args, **kwargs):
        """
        :param:

         - `master`: The master Builder (builder.py)
         - `config_map`: A populated configuration map
         - `previous_parameters`: A list of the parameters created by previous builders
        """
        super(WatcherBuilder, self).__init__(*args, **kwargs)
        self._watchers = None
        self._watcher_ids = None
        return

    @property
    def watcher_ids(self):
        """
        :return: list of options from the Watch Log config section 
        """
        if self._watcher_ids is None:
            self._watcher_ids = self.config_map.options(ConfigOptions.watchlogs_section)
        return self._watcher_ids

    @property
    def watchers(self):
        """
        :rtype: ListType 
        :return: A list of watchers
        """
        if self._watchers is None:
            self._watchers = []
            for watch_id in self.watcher_ids:
                parameters = self.config_map.get_namedtuple(ConfigOptions.watchlogs_section,
                                                            watch_id)
                builder = watcher_builder[parameters.type]
                for name, node in self.master.thread_nodes.iteritems():
                    watcher = builder(node=node, parameters=parameters,
                                      output=self.master.storage, name=name).product
                    self._watchers.append(watcher)
        return self._watchers

    @property
    def product(self):
        """
        :rtype: TheWatcher
        :return: A master watcher 
        """
        if self._product is None:
            self._product = thewatcher.TheWatcher(watchers=self.watchers)
        return self._product

    @property
    def parameters(self):
        """
        Returns the previous_parameters
        """
        if self._parameters is None:
            self._parameters = self.previous_parameters
        return self._parameters
# end class LogwatchersBuilder
