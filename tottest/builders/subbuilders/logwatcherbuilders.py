"""
A module to build logwatchers
"""

class LogcatWatcherBuilder(object):
    """
    A builder of logcat watchers
    """
    def __init__(self, node, parameters):
        """
        :param:

         - `node`: device to watch        
         - `parameters`: named tuple built from config file
        """
        self.node = node
        self.parameters = parameters
        return
# end class LogcatWatcherBuilder
