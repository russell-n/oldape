"""
A module to hold an iperf test tool
"""

# tottest
from tottest.baseclass import BaseClass


class IperfTest(BaseClass):
    """
    The Iperf Test runs a single iperf test.
    """
    def __init__(self, sender, receiver, killers):
        """
        :param:

         - `sender`: IperfCommand configured as sender
         - `receiver`: IperfCommand configured as receiver
         - `killers`: An iterable of Iperf Killers
        """
        super(IperfTest, self).__init__()
        self.sender = sender
        self.receiver = receiver
        self.killers = killers
        return
    
    def run(self, parameters):
        
        return

# end class IperfTest
