#python
from unittest import TestCase
from socket import timeout

#third-party
from mock import MagicMock
from nose import tools
raises = tools.raises

from apetools.affectors.elexol import naxxx
from apetools.affectors.elexol import errors

FaucetteError = errors.FaucetteError
NaxxxError = naxxx.NaxxxError


class TestNaxxx(TestCase):
    def setUp(self):
        self.hostname = "192.168.12.60"
        self.clear = True
        self.retries = 12
        self.naxxx = naxxx.Naxxx(self.hostname,
                                 self.clear,
                                 self.retries)
        self.naxxx._naxxx = MagicMock()
        return

    def test_clean_outlets_castable(self):
        identifier = "3"
        outlets = self.naxxx._clean_outlets(identifier)
        self.assertEqual(int(identifier), outlets[0])
        return

    def test_clean_outlets_list(self):
        identifier = "3"
        identifiers = [identifier]
        outlets = self.naxxx._clean_outlets(identifiers)
        self.assertEqual(int(identifier), outlets[0])
        return

    @raises(FaucetteError)
    def test_clean_outlets_list_error(self):
        outlets = self.naxxx._clean_outlets('a')
        return

    def test_run(self):
        identifier = 3
        self.naxxx.run(3)
        self.naxxx._naxxx.turn_on_switches.assert_called_with([identifier], turn_others_off=True)
        return

    @raises(NaxxxError)
    def test_naxxx_error(self):
        self.naxxx._naxxx.turn_on_switches.side_effect = TypeError("'NoneType' object has no attribute '__getitem__'")
        self.naxxx.run(3)
        return

    @raises(NaxxxError)
    def test_socket_error(self):
        self.naxxx._naxxx.turn_on_switches.side_effect = timeout("socket timeout")
        self.naxxx.run(3)
        return
# end class TestNaxxx
