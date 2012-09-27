from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock

from tottest.builders.subbuilders.executetestbuilder import ExecuteTestBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.executetest import DummyExecuteTest

class TestExecuteTestBuilder(TestCase):
    def setUp(self):
        config_map = ConfigurationMap("")
        self.parser = MagicMock()
        self.master = MagicMock()
        config_map._parser = self.parser
        self.builder = ExecuteTestBuilder(self.master, config_map, [])
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "test")
        actual = self.builder.product
        self.assertIsInstance(actual, DummyExecuteTest)
        return
# end class ExecutetestBuilder
