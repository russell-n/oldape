from unittest import TestCase
from mock import MagicMock, patch


class TestRotator(TestCase):
    def test_import(self):
        rate_table = MagicMock()
        with patch("RateTable", rate_table):
            import apetools.affectors.rotator.rotator 
            rotator = apetools.affectors.rotator.rotator.Rotator()
