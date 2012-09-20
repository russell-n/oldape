from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock

from tottest.builders.subbuilders.operationsetupbuilder import OperationSetupBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.operationsetup import DummySetupOperation

class TestSetupOperationBuilder(TestCase):
    def setUp(self):
        config_map = ConfigurationMap("")
        self.parser = MagicMock()
        config_map._parser = self.parser
        self.builder = OperationSetupBuilder(config_map)
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "operation_setup")
        actual = self.builder.operation_setup
        self.assertIsInstance(actual, DummySetupOperation)
        return
# end class TestSetupOperationBuilder
