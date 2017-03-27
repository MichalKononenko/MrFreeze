# -*- coding: utf-8 -*-
"""
Contains unit tests for the bootloader
"""
import unittest
import unittest.mock as mock
from mr_freeze import BootLoader


class TestBootloader(unittest.TestCase):
    """
    Contains unit tests for the bootloader
    """
    def setUp(self):
        self.loader = BootLoader()


class TestConfigFileName(TestBootloader):
    """
    Check that the bootloader correctly identifies a config file
    """
    def setUp(self):
        TestBootloader.setUp(self)
        self.expected_correct_path = self.loader.CONFIG_FILE_LOCATIONS[0]

    @mock.patch('mr_freeze.bootstrap.os.path.isfile', return_value=True)
    def test_config_file_first_is_true(self, mock_file_predicate):
        self.assertEqual(
            self.expected_correct_path,
            self.loader.config_file_name
        )
        self.assertEqual(
            mock.call(self.expected_correct_path),
            mock_file_predicate.call_args
        )

    @mock.patch('mr_freeze.bootstrap.os.path.isfile', return_value=False)
    def test_config_no_file(self, mock_file_predicate):
        self.assertIsNone(self.loader.config_file_name)
        self.assertTrue(
            mock_file_predicate.called
        )
