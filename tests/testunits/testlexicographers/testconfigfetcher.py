from unittest import TestCase
import os

from tottest.lexicographers import configfetcher

class TestConfigFetcher(TestCase):
    def setUp(self):
        self.fetcher = configfetcher.ConfigFetcher()
        self.folder_path = os.path.join(__import__(configfetcher.__package__).__path__[0], "lexicographers/configfiles") 
        return

    def test_config_folder_path(self):
        self.assertEqual(self.folder_path, self.fetcher.config_folder_path)
        return

    def test_config_names(self):
        for name in self.fetcher.config_names():
            self.assertEqual("throughputovertime.ini", name)
