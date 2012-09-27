from unittest import TestCase

from mock import MagicMock

from tottest.builders.subbuilders.nersbuilder import NersBuilder
from tottest.affectors.ners import NeRS

class TestNersBuilder(TestCase):
    def setUp(self):
        self.master = MagicMock()
        self.config_map = MagicMock()
        self.builder = NersBuilder(self.master, self.config_map, [])
        return

    def test_product(self):
        product = self.builder.product
        self.assertIsInstance(product, NeRS)
        return

    def test_parameters(self):
        nodes = {"a":1, "b":2}
        self.master.nodes = nodes
        parameters = self.builder.parameters
        for parameter in parameters:
            self.assertEqual("nodes", parameter.name)
# end class TestNersBuilder
             
