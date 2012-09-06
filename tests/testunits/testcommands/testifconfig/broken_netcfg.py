from StringIO import StringIO
from mock import MagicMock
from tottest.commands import netcfg
#from tottest.commons import enumerations

from ..common import assert_equal


def test():
    # mock a local linux connection
    connection = MagicMock()
    connection.netcfg.return_value = StringIO(netcfg_android)

    ncf = netcfg.NetcfgCommand(connection,
                               'wlan0')
    #assert_equal(connection.ifconfig.return_value, ifc.output)
    assert_equal("192.168.20.153", ncf.ip_address)
    assert_equal("f0:a2:25:1f:09:0d", ncf.mac_address)
    return

netcfg_android = """
lo       UP                                   127.0.0.1/8   0x00000049 00:00:00:00:00:00
ifb0     DOWN                                   0.0.0.0/0   0x00000082 e2:ae:7a:12:eb:a2
ifb1     DOWN                                   0.0.0.0/0   0x00000082 fe:7b:1d:2a:cf:2a
sit0     DOWN                                   0.0.0.0/0   0x00000080 00:00:00:00:00:00
ip6tnl0  DOWN                                   0.0.0.0/0   0x00000080 00:00:00:00:00:00
wlan0    UP                              192.168.20.153/24  0x00001043 f0:a2:25:1f:09:0d
"""

if __name__ == "__main__":
    import pudb; pudb.set_trace()
    test()
