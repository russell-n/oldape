
# python standard-library
from collections import namedtuple

# this package
from apetools.baseclass import BaseClass


APParameters = namedtuple("APParameters", "name node ssid")


class APConnect(BaseClass):
    """
    A class to connect a device to an AP
    """
    def __init__(self, nodes):
        """
        :param:

         - `nodes`: dictionary of id:device pairs
        """
        super(APConnect, self).__init__()
        self.nodes = nodes
        return

    def __call__(self, parameters):
        """
        :param:

         - `parameters`: a named tuple with `nodes.parameters` and `ssids.parameters` attributes
         """
        self.logger.info("Connecting '{0}' to SSID: '{1}'".format(parameters.nodes.parameters,
                                                                  parameters.ssids.parameters))
        self.nodes[parameters.nodes.parameters].connect(parameters.ssids.parameters)
        return
# end class APConnect       
