from unittest import TestCase
import ConfigParser

from mock import MagicMock

from tottest.builders.subbuilders.nodesbuilder import NodesBuilder
from tottest.lexicographers.configurationmap import ConfigurationMap
from tottest.lexicographers.config_options import ConfigOptions
from tottest.devices.dummydevice import DummyDevice
from tottest.devices.windowsdevice import WindowsDevice


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

    def test_windows(self):
        self.parser.options.return_value = "igor eyegore".split()
        def side_effect(*args):
            if args == (ConfigOptions.nodes_section, "igor"):
                return "connection:SSH, operating_system:windows, hostname:igor, login:developer"
            elif args == (ConfigOptions.nodes_section, "eyegore"):
                return "connection:ssh, operating_system:Windows, hostname:eyegore, login:allion, password:testlabs"
            return

        self.parser.get.side_effect = side_effect
        for device in self.builder.nodes:
            self.assertIsInstance(self.builder.nodes[device], WindowsDevice)
# class TestNodesBuilder
