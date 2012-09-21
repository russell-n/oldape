from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock
from tottest.builders.subbuilders.setuptestbuilder import SetupTestBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.setuptest import SetupTest
from tottest.operations.setuptest import DummySetupTest

class TestSetupTestBuilder(TestCase):
    def setUp(self):
        self.master = MagicMock()
        self.parser = MagicMock()
        self.config_map = ConfigurationMap("")
        self.config_map._parser = self.parser
        self.builder = SetupTestBuilder(master=self.master,
                                        config_map=self.config_map)
        return

    def test_plans(self):
        expected = "a b c".split()
        self.parser.get.return_value = "a,b,c"
        actual = self.builder.plans
        self.assertEqual(expected, actual)
        return
    
    def test_product(self):
        self.parser.get.return_value = "ners"
        product = self.builder.product
        self.assertIsInstance(product, SetupTest)
        return

    def test_parameters(self):
        self.parser.get.return_value = "ners"
        self.master.nodes = {"a":1, "b":2, "c":3}
        parameters = self.builder.parameters
        for parameter in parameters:
            self.assertEqual("ners", parameter.name)
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "test_setup")
        actual = self.builder.product
        self.assertIsInstance(actual, DummySetupTest)
        return
# end class TestSetupTestBuilder
