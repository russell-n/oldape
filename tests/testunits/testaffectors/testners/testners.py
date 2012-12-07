from unittest import TestCase
from string import letters
from random import randint, choice
from collections import namedtuple

from mock import MagicMock

from apetools.affectors import ners

EMPTY_STRING = ""

Parameters = namedtuple("Parameters", 'name parameters'.split())
Parameter = namedtuple("Parameter", "ners")


def get_nodes():
    node_count = randint(1,100)
    nodes = {}
    for node in range(node_count):
        address = EMPTY_STRING.join([choice(letters) for c in range(randint(1, 10))])
        nodes[address] = MagicMock()
    return nodes

class TestNers(TestCase):
    def setUp(self):
        self.nodes = get_nodes()
        self.ners = ners.NeRS(self.nodes)
        return

    #def test_enable(self):
    #    count = randint(1, len(self.nodes))
    #    addresses = Parameter("nodes", [choice(self.nodes.keys()) for c in range(count)])
    #    self.ners(addresses)
    #    for address in addresses.ners.parameters:
    #        self.nodes[address].enable_wifi.assert_called_with()
    #    for address in set(self.nodes.keys()).difference(set(addresses.ners.parameters)):
    #        self.nodes[address].disable_wifi.assert_called_with()
    #    return
# end class TestNers
