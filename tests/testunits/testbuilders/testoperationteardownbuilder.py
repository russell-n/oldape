from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock

from tottest.builders.subbuilders.operationteardownbuilder import OperationTeardownBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.operationteardown import DummyTeardownOperation

class TestTeardownOperationBuilder(TestCase):
    def setUp(self):
        config_map = ConfigurationMap("")
        self.parser = MagicMock()
        self.master = MagicMock()
        config_map._parser = self.parser
        self.builder = OperationTeardownBuilder(self.master, config_map, [])
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "operation_teardown")
        actual = self.builder.product
        self.assertIsInstance(actual, DummyTeardownOperation)
        return
# end class TestTeardownOperationBuilder
