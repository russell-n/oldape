from unittest import TestCase
from mock import MagicMock, patch


class TestRotator(TestCase):
    def test_import(self):
        rate_table = MagicMock()
        with patch("RateTable", rate_table):
            import tottest.affectors.rotator.rotator 
            rotator = tottest.affectors.rotator.rotator.Rotator()
