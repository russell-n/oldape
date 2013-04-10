from unittest import TestCase
from collections import namedtuple

from mock import MagicMock

from apetools.lexicographers import configurationmap


ConfigurationMap = configurationmap.ConfigurationMap


class ConfigurationMapTest(TestCase):
    def setUp(self):
        self.parser = MagicMock()
        self.map = ConfigurationMap("name")
        self.map._parser = self.parser
        return

    def test_get_ranges(self):
        self.map.get_list = MagicMock()
        self.map.get_list.return_value = ['1-3']
        ranges = self.map.get_ranges("NAXXX", "switches")
        self.assertEqual(ranges, [1,2,3])
        self.map.get_list.return_value = None
        ranges = self.map.get_ranges("NAXXX", 's', optional=True)
        self.assertEqual(ranges, None)
        self.map.get_list.return_value = ['2-5', '10', '3-12']
        ranges = self.map.get_ranges('NAXXX', 'switches')
        self.assertEqual(ranges, [2,3,4,5,10,3,4,5,6,7,8,9,10,11,12])
        return

    def test_get_list(self):
        value = "3,4,5"
        self.map._parser.get.return_value = value
        output = self.map.get_list("DUT", "ids")
        self.assertEqual(value.split(','), output)
        return

    def test_get_list_optional(self):
        value = None
        self.map._parser.get.return_value = value
        output = self.map.get_list("DUT", "paths", optional=True)
        self.assertEqual(value, output)
        return

    def test_get_named_tuple(self):
        self.map._parser.get.return_value = "cow:boy,hot:dog, pig:face"
        section = "SECTION"
        option = "notanoption"
        t = namedtuple(option, "cow hot pig".split())
        expected = t("boy", "dog",  "face")
        actual = self.map.get_namedtuple(section, option)
        for field in actual._fields:
            self.assertEqual(getattr(expected, field), getattr(actual, field))
        return

if __name__ == "__main__":
    import pudb
    pudb.set_trace()
    _map = ConfigurationMap("name")
    _map.get_list = MagicMock()
    _map.get_list.return_value = ['1-3']
    ranges = _map.get_ranges("NAXXX", "switches")
    assert ranges == [1,2,3]
    _map.get_list.return_value = None
    ranges = _map.get_ranges("NAXXX", 's', optional=True)
    assert ranges == None
    _map.get_list.return_value = ['2-5', '10', '3-12']
    ranges = _map.get_ranges('NAXXX', 'switches')
    assert ranges == [2,3,4,5,10,3,4,5,6,7,8,9,10,11,12]
    
