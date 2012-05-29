from mock import MagicMock
from tottest.commands import ifconfig
from tottest.commons import enumerations

# mock a local linux connection
connection = MagicMock()
connection.ifconfig.return_value = open("ifconfig.linux")
connection_android = MagicMock()
connection_android.ifconfig.return_value = open("ifconfig.android")

def assert_equal(expected, actual):
    assert expected == actual, "Expected: {0} Actual: {1}".format(expected, actual)

def testlinux():
    ifc = ifconfig.IfconfigCommand(connection, 'eth0')
    #assert_equal(connection.ifconfig.return_value, ifc.output)
    assert_equal("192.168.10.50", ifc.ip_address)
    assert_equal( "00:26:2d:29:a1:8e", ifc.mac_address)
    return

def testandroid():
    ifc = ifconfig.IfconfigCommand(connection_android, "wlan0",
                                   enumerations.OperatingSystem.android)
    assert_equal("192.168.20.153", ifc.ip_address)
    assert_equal(ifconfig.MAC_UNAVAILABLE, ifc.mac_address)
    return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    testlinux()
    testandroid()
