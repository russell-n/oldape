# python standard library
from unittest import TestCase

# third-party
from mock import MagicMock

#tottest
from tottest.watchers.fileexpressionwatcher import FileExpressionWatcher


class TestFileExpressionWatcher(TestCase):
    def setUp(self):
        self.output = MagicMock()
        self.connection = MagicMock()
        return
