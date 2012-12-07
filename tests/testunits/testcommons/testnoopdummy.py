from unittest import TestCase

from mock import MagicMock

from apetools.commons import dummy


class TestDummy(TestCase):
    def setUp(self):
        self.name = "Dummy"
        self.parameters = "cow"
        self.dummy = dummy.NoOpDummy(name=self.name)
        return

    def test_run(self):
        self.dummy._logger = MagicMock()
        self.dummy.run(self.parameters)
        self.dummy.logger.debug.assert_called_with(dummy.LOG_STRING.format(self.name, self.parameters))
        return
# end class TestDummy
                
