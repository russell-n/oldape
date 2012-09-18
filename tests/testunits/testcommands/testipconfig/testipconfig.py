from unittest import TestCase
from StringIO import StringIO

from mock import MagicMock

from tottest.commands.ipconfig import Ipconfig
from tottest.connections.localconnection import OutputError

output = """
Windows IP Configuration


Wireless LAN adapter Wireless Network Connection 3:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Wireless LAN adapter Wireless Network Connection 2:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Wireless LAN adapter Wireless Network Connection:

   Connection-specific DNS Suffix  . : testnetwork.local
   Link-local IPv6 Address . . . . . : fe80::3988:30da:5414:8180%12
   IPv4 Address. . . . . . . . . . . : 192.168.20.99
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : fe80::226:5aff:feff:4294%12
                                       192.168.20.1

Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . : 
   Link-local IPv6 Address . . . . . : fe80::495a:6a04:eded:5daf%11
   IPv4 Address. . . . . . . . . . . : 192.168.10.63
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.10.1

Tunnel adapter isatap.{9703F5B2-AE1F-493C-8B6A-1231760A6A63}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Tunnel adapter isatap.testnetwork.local:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Tunnel adapter isatap.{D46350ED-E789-4453-A0B9-8B6CFF700B00}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Tunnel adapter isatap.{754E07B6-882B-4D20-BB0B-356E6D324B43}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

Tunnel adapter Teredo Tunneling Pseudo-Interface:

   Connection-specific DNS Suffix  . : 
   IPv6 Address. . . . . . . . . . . : 2001:0:4137:9e76:1051:d59:3f57:eb9c
   Link-local IPv6 Address . . . . . : fe80::1051:d59:3f57:eb9c%15
   Default Gateway . . . . . . . . . : ::
"""

DISABLED = """
Windows IP Configuration


Ethernet adapter Local Area Connection:

   Connection-specific DNS Suffix  . :
   Link-local IPv6 Address . . . . . : fe80::495a:6a04:eded:5daf%11
   IPv4 Address. . . . . . . . . . . : 192.168.10.63
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 192.168.10.1

Tunnel adapter isatap.{9703F5B2-AE1F-493C-8B6A-1231760A6A63}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Tunnel adapter isatap.testnetwork.local:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Tunnel adapter isatap.{D46350ED-E789-4453-A0B9-8B6CFF700B00}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Tunnel adapter isatap.{754E07B6-882B-4D20-BB0B-356E6D324B43}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . :

Tunnel adapter Teredo Tunneling Pseudo-Interface:

   Connection-specific DNS Suffix  . :
   IPv6 Address. . . . . . . . . . . : 2001:0:4137:9e76:83:15ea:3f57:f5c0
   Link-local IPv6 Address . . . . . : fe80::83:15ea:3f57:f5c0%15
   Default Gateway . . . . . . . . . : ::
"""

class TestIpconfig(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = Ipconfig(self.connection)
        return

    def test_expression(self):
        line = "   IPv4 Address. . . . . . . . . . . : 192.168.20.99"
        self.assertRegexpMatches(line, self.command.ip_expression)
        return
        
    def test_ip(self):
        expected = "192.168.20.99"
        self.connection.ipconfig.return_value = OutputError(StringIO(output), "")
        actual = self.command.address
        self.assertEqual(expected, actual)
        return

    def test_disabled(self):
        self.connection.ipconfig.return_value = OutputError(StringIO(DISABLED), "")
        self.assertEqual(self.command.not_available, self.command.address)
        return
    
# end class TestIpconfig
