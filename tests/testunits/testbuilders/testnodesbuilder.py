from unittest import TestCase
import ConfigParser

from mock import MagicMock

from tottest.builders.subbuilders.nodesbuilder import NodesBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.devices.dummydevice import DummyDevice


class TestNodesBuilder(TestCase):
    def setUp(self):
        self.builder = MagicMock()
        self.parser = MagicMock()
        config = ConfigurationMap("")
        config._parser = self.parser
        self.builder = NodesBuilder(self.builder, config)
        return

    def test_dummy(self):
        self.parser.options.side_effect = ConfigParser.NoSectionError("No such section")
        for device in self.builder.nodes:
            self.assertIsInstance(self.builder.nodes[device], DummyDevice)
        return
# class TestNodesBuilder
