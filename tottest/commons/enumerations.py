"""
Not really a place for enumerations so much as classes that act like them.
"""

class OperatingSystem(object):
    """
    The Operating System holds constant names for operating systems
    """
    __slots__ = ()
    linux = "linux"
    android = "android"
    windows = "windows"
# end class OperatingSystem


TO_DUT = 't'
FROM_DUT = 'f'

class IperfDirection(object):
    """
    The IperfDirection holds constant values for the direction of iperf traffic.

    To accomodate the confusing number of terms people use at allion, the following are aliased:

     * to_dut = downlink = receive = rx
     * from_dut = uplink = transmit = tx = send
    """
    __slots__ = ()
    to_dut = TO_DUT
    downlink = TO_DUT
    receieve = TO_DUT
    rx = TO_DUT
    
    from_dut = FROM_DUT
    uplink = FROM_DUT
    transmit = FROM_DUT
    tx = FROM_DUT
    send = FROM_DUT
# end class IperfDirection
    
