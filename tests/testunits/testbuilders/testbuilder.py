#python
from unittest import TestCase
from threading import RLock
from ConfigParser import NoOptionError

#third-party
from mock import MagicMock

#tottest
from tottest.builders import builder
from tottest.proletarians import hortator
from tottest.lexicographers.configurationmap import ConfigurationMap

# Dummies
from tottest.operations.operationsetup import DummySetupOperation
from tottest.operations.operationteardown import DummyTeardownOperation
from tottest.operations.setuptest import DummySetupTest
from tottest.operations.executetest import DummyExecuteTest
from tottest.operations.teardowntest import DummyTeardownTest

class TestBuilder(TestCase):
    def setUp(self):
        self.parser = MagicMock()
        config = ConfigurationMap("")
        config._parser = self.parser
        self.builder = builder.Builder([config])
        return

    def test_lock(self):
        self.assertIs(type(RLock()), type(self.builder.lock))
        return

    def test_hortator(self):
        #self.builder._operators = MagicMock()
        h = self.builder.hortator
        self.assertIs(hortator.Hortator, type(h))
        return

    def test_dummy_operator(self):
        self.parser.get.side_effect = NoOptionError("option", "Test")
        for operator in self.builder.operators:
            self.assertIsInstance(operator.operation_setup, DummySetupOperation)
            self.assertIsInstance(operator.operation_teardown, DummyTeardownOperation)
            self.assertIsInstance(operator.test_setup, DummySetupTest)
            self.assertIsInstance(operator.tests, DummyExecuteTest)
            self.assertIsInstance(operator.test_teardown, DummyTeardownTest)
        return

    def test_reset(self):
        config = ConfigurationMap("")
        config._parser = self.parser
        b = builder.Builder([config])
        b.current_config = config
        self.parser.get.side_effect = NoOptionError("option", "Test")
        self.assertIsNotNone(b.operation_setup_builder(config))
        self.assertIsNotNone(b.operation_teardown_builder(config))
        self.assertIsNotNone(b.setup_test_builder(config))
        self.assertIsNotNone(b.execute_test_builder(config))
        self.assertIsNotNone(b.teardown_test_builder(config))
        self.assertIsNotNone(b.storage(config))
        self.assertIsNotNone(b.nodes(config))
        self.assertIsNotNone(b.lock)
        return
