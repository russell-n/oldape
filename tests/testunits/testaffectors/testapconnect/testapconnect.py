from unittest import TestCase
from collections import namedtuple

from mock import MagicMock

from apetools.affectors.apconnect import APConnect

Parameter = namedtuple("Parameter", 'nodes parameters'.split())
Parameters = namedtuple("Parameters", 'address parameters'.split())

class TestApConnect(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.device = MagicMock()
        self.nodes = {"alpha":self.device}
        self.affector = APConnect(self.nodes)
        return

    #def test_call(self):
    #    self.connection.netsh.return_value = ""
    #    p = Parameter("nodes", "allionstaff")
    #    self.affector(p)
    #    self.device.connect.assert_called_with("allionstaff")
    #    
    #    return
# end class TestApConnect
