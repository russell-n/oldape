from StringIO import StringIO
from mock import MagicMock
from tottest.commands import ifconfig
from tottest.commons import enumerations

def assert_equal(expected, actual):
    assert expected == actual, "Expected: {0} Actual: {1}".format(expected, actual)

def testlinux():
    connection = MagicMock()
    connection.ifconfig.return_value = StringIO(ifconfig_linux)

    ifc = ifconfig.IfconfigCommand(connection, 'eth0')
    #assert_equal(connection.ifconfig.return_value, ifc.output)
    assert_equal("192.168.10.50", ifc.ip_address)
    assert_equal( "00:26:2d:29:a1:8e", ifc.mac_address)
    return

def testandroid():
    connection = MagicMock()
    connection.ifconfig.return_value = StringIO(ifconfig_android)

    ifc = ifconfig.IfconfigCommand(connection, "wlan0",
                                   enumerations.OperatingSystem.android)
    assert_equal("192.168.20.153", ifc.ip_address)
    assert_equal(ifconfig.MAC_UNAVAILABLE, ifc.mac_address)
    return

ifconfig_linux = '''
eth0      Link encap:Ethernet  HWaddr 00:26:2d:29:a1:8e  
          inet addr:192.168.10.50  Bcast:192.168.10.255  Mask:255.255.255.0
          inet6 addr: fe80::226:2dff:fe29:a18e/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:715528 errors:0 dropped:0 overruns:0 frame:0
          TX packets:282106 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:392919899 (392.9 MB)  TX bytes:22980409 (22.9 MB)
          Interrupt:18 

'''

ifconfig_android = """
wlan0: ip 192.168.20.153 mask 255.255.255.0 flags [up broadcast running multicast]
"""

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    testlinux()
    testandroid()
