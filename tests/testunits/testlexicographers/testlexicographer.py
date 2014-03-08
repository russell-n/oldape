from random import choice, randint
from unittest import TestCase
from string import letters
from StringIO import StringIO

from nose.tools import raises
from mock import MagicMock, patch

from apetools.lexicographers import lexicographer
from apetools.lexicographers.configurationmap import ConfigurationMap

from apetools.commons import errors

ConfigurationError = errors.ConfigurationError
ArgumentError = errors.ArgumentError
import tot

def get_string():
    return "".join([choice(letters) for i in range(randint(1, 10))])

listdir = MagicMock()

class TestNewLexicographer(TestCase):
    def setUp(self):
        # the Configuration map will try to open the filename it's given
        handle = MagicMock(spec=file)
        handle.read.return_value = StringIO(tot.output)
        self.open_mock = MagicMock(return_value = handle)

        # fake the names found
        self.filenames = [get_string() for i in range(randint(1,10))]
        self.glob = 'tot.ini'
        self.lex = lexicographer.Lexicographer(self.glob)
        self.shallow_find = MagicMock(return_value=self.filenames)
        self.lex._finder = self.shallow_find
        return

    def test_filenames(self):
        """
        the filenames property yields what the shallow_find function finds
        """
        self.lex._finder = self.filenames

        actual = [name for name in self.lex.filenames]
        self.assertEqual(self.filenames, actual)
        return

    @raises(ArgumentError)
    def test_no_filenames(self):
        """
        If no files match the glob an ArgumentError is raised
        """
        self.lex._finder = MagicMock(return_value = [])
        for name in self.lex.filenames:
            pass
        self.lex._finder = None
        return
    
    def test_iteration(self):
        """
        The Lexicographer yields configuration maps for each file
        """
        self.lex._finder = self.shallow_find.return_value
        
        with patch('__main__.open', self.open_mock, create=True):
            lexes = [l for l in self.lex]
        expected = len(self.filenames)
        actual = len(lexes)
        self.assertEqual(expected,actual)
        for l in lexes:
            self.assertIsInstance(l, ConfigurationMap)
        return
# end class TestNewLexicographer

if __name__ == "__main__":
    import pudb
    pudb.set_trace()

    filenames = "a b c".split()
    shallow_find = MagicMock(return_value=filenames)
    lexicographer.shallow_find = shallow_find
    glob = 'tot.ini'
    lex = lexicographer.Lexicographer(glob)
    
    actual = [name for name in lex.filenames]
    
