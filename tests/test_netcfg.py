from mock import MagicMock
from tottest.commands import netcfg
#from tottest.commons import enumerations

from common import assert_equal

# mock a local linux connection
connection = MagicMock()
connection.netcfg.return_value = open("netcfg.android")

def test():
    ncf = netcfg.NetcfgCommand(connection,
                               'wlan0')
    #assert_equal(connection.ifconfig.return_value, ifc.output)
    assert_equal("192.168.20.153", ncf.ip_address)
    assert_equal("f0:a2:25:1f:09:0d", ncf.mac_address)
    return

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test()
