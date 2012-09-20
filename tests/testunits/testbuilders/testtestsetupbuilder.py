from unittest import TestCase
from ConfigParser import NoOptionError

from mock import MagicMock

from tottest.builders.subbuilders.setuptestbuilder import SetupTestBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.operations.setuptest import DummySetupTest

class TestSetupTestBuilder(TestCase):
    def setUp(self):
        config_map = ConfigurationMap("")
        self.parser = MagicMock()
        config_map._parser = self.parser
        self.builder = SetupTestBuilder(config_map)
        return

    def test_dummy(self):
        self.parser.get.side_effect = NoOptionError("TEST", "test_setup")
        actual = self.builder.test_setup
        self.assertIsInstance(actual, DummySetupTest)
        return
# end class TestSetuptestBuilder
