
# python standard library
from collections import namedtuple


class IperfTestParameters(namedtuple("IperfTestParameters", ["filename",
                                                             "iperf_parameters"])):
    """
    IperfTestParameters add a filename to the iperf parameters.
    """
    def __str__(self):
        """
        :return: string representation of iperf_parameters
        """
        return str(self.iperf_parameters)
# end class IperfTestParameters
