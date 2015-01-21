
from apetools.baseclass import BaseClass


class DumpDeviceState(BaseClass):
    """
    A class to record the state of a device.
    """
    def __init__(self, devices, target=None):
        """
        :param:

         - `devices`: a dictionary of id:device pairs
         - `target`: optional callable object to pass output
        """
        super(DumpDeviceState, self).__init__()
        self.devices = devices
        self.target = target
        return

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: a named tuple (expects parameters.nodes.parameters)
        """
        device = self.devices[parameters.nodes.parameters]
        self.logger.info(str(device))
        if self.target is not None:
            self.target(str(device))
        return
# end class DumpDeviceState
