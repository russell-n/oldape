"""
A configurer and queryier for linux devices.
"""

class LinuxDevice(object):
    """
    A class to configure and query linux devices
    """
    def __init__(self, connection):
        self.connection = connection
        return
# end class LinuxDevice
