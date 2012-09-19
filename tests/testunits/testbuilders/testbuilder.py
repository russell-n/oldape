#python
from unittest import TestCase
from threading import RLock

#third-party
from mock import MagicMock

#tottest
from tottest.builders import builder
from tottest.proletarians import hortator



class TestBuilder(TestCase):
    def setUp(self):
        self.parameters = MagicMock()
        self.builder = builder.Builder(self.parameters)
        return

    def test_lock(self):
        self.assertIs(type(RLock()), type(self.builder.lock))
        return

    def test_hortator(self):
        #self.builder._operators = MagicMock()
        h = self.builder.hortator
        self.assertIs(hortator.Hortator, type(h))
        return

