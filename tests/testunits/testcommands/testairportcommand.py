# python standard library
from unittest import TestCase
from StringIO import StringIO

#third-party
from mock import MagicMock

#apetools
from apetools.commands.airportcommand import AirportCommand

OUTPUT = """
     agrCtlRSSI: -79
     agrExtRSSI: 0
    agrCtlNoise: -89
    agrExtNoise: 0
          state: running
        op mode: station 
     lastTxRate: 216
        maxRate: 450
lastAssocStatus: 0
    802.11 auth: open
      link auth: wpa2-psk
          BSSID: 84:1b:5e:da:34:8
           SSID: r6300_5
            MCS: 13
        channel: 36,1
"""

class TestAirport(TestCase):
    def setUp(self):
        self.connection = MagicMock()
        self.command = AirportCommand(connection=self.connection,
                                      interface='wlan0')
        return

    def try_value(self, field, expected):
        self.connection.airport.return_value = StringIO(OUTPUT), StringIO('')
        actual = getattr(self.command, field)
        self.assertEqual(expected, actual)
        return

    
    def test_bitrate(self):
        self.try_value('bitrate', '450')
        return

    def test_rssi(self):
        self.try_value('rssi', '-79')
        return

    def test_channel(self):
        self.try_value('channel', '36,1')
        return

    def test_noise(self):
        self.try_value('noise', '-89')

    def test_bssid(self):
        self.try_value('bssid', '84:1b:5e:da:34:8')

    def test_ssid(self):
        self.try_value('ssid', 'r6300_5')


    def test_string(self):
        self.connection.airport.return_value = StringIO(OUTPUT)
        actual = str(self.command)
        self.assertEqual(OUTPUT,actual)
        self.connection.airport.assert_called_with('airport --getinfo')
        return
    # end TestAirport
