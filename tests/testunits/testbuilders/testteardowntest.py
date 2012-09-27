from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock

from tottest.builders.subbuilders.teardowntestbuilder import TeardownTestBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.teardowntest import DummyTeardownTest

class TestTeardownTestBuilder(TestCase):
    def setUp(self):
        config_map = ConfigurationMap("")
        self.parser = MagicMock()
        self.master = MagicMock()
        config_map._parser = self.parser
        self.builder = TeardownTestBuilder(self.master, config_map, [])
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "test_teardown")
        actual = self.builder.product
        self.assertIsInstance(actual, DummyTeardownTest)
        return
# end class TestTeardownTestBuilder
