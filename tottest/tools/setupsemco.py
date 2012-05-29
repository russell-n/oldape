"""
A tool to setup the semco settop box for testing.
"""

from tottest.baseclass import BaseClass


class SetupSemco(BaseClass):
    """
    A SetupSemco Sets up the semco
    """
    def __init__(self, connection, ssid, password):
        """
        :param:

         - `connection`: A connection to the device
         - `ssid`: The ssid of the AP To connect to
         - `password`: The password of the AP
        """
        super(SetupSemco, self).__init__()
        self.connection = connection
        return

    def run(self):
        """
        Runs the start and connect sequence.
        """
# end SetupSemco
