"""
A builder of logwatchers
"""

#tottest
from basetoolbuilder import BaseToolBuilder
from logwatcherbuilders import LogcatWatcherBuilder
from tottest.watchers import thewatcher

from tottest.lexicographers.config_options import ConfigOptions

class WatcherTypes(object):
    """
    The names of the valid watcher types
    """
    __slots__ = ()
    logcat = "logcat"
# end class WatcherTypes

    
watcher_builder = {WatcherTypes.logcat:LogcatWatcherBuilder}

class WatchLogsBuilder(BaseToolBuilder):
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
        super(WatchLogsBuilder, self).__init__(*args, **kwargs)
        self._watchers = None
        self._watcher = None
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
                for node in self.master.thread_nodes:
                    watcher = builder(node, parameters).product
                    self._watchers.append(watcher)
        return self._watchers

    @property
    def watcher(self):
        """
        :rtype: TheWatcher
        :return: A master watcher 
        """
        if self._watcher is None:
            self._watcher = thewatcher.TheWatcher(watchers=self.watchers)
        return self._watcher
# end class LogwatchersBuilder
