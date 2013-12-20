"""
The Iperf Test Parameters are a place to add extra information that has to be passed in to the IperfCommand
"""

from collections import namedtuple


class IperfTestParameters(namedtuple("IperfTestParameters", "filename iperf_parameters".split())):
    """
    IperfTestParameters add a filename while maintaining the __str__ of the iperf parameters.
    """
    def __str__(self):
        return str(self.iperf_parameters)
# end class IperfTestParameters
