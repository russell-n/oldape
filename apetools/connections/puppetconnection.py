
from localconnection import LocalConnection


class PuppetConnection(LocalConnection):
    """
    A puppet connection holds methods to affect the attached device.
    """
    def __init__(self, *args, **kwargs):
        super(PuppetConnection, self).__init__(*args, **kwargs)
        return

    def add_paths(self, paths):
        """
        
        """
        output, error = self._main("echo", "'$PATH'")
        default = output.readline().rstrip()
        paths = ":".join([path for path in paths if path not in default])
        output, error = self._main("PATH={0}:{1}".format(paths, default))
        return
# end class PuppetConnection
