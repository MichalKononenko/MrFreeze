# -*- coding: utf-8 -*-
"""
Contains unit tests for the bootloader
"""
import unittest
import unittest.mock as mock
from typing import Mapping
from mr_freeze import BootLoader
from mr_freeze.exceptions import BadConfigParameter
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510

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


class OverloadedBootLoaderTestCase(TestBootloader):
    """
    Base class for unit tests requiring a bootloader that has "read" a
    configuration file
    """

    def setUp(self):
        TestBootloader.setUp(self)
        self.parameters = {'GAUSSMETER_ADDRESS': 'address'}

        self.loader = self.OverloadedConfigBootLoader(self.parameters)

    class OverloadedConfigBootLoader(BootLoader):
        """
        Describes a bootlaoder that doesn't actually look for the config
        file, but returns a dict instead
        """
        def __init__(self, params):
            super().__init__()
            self._params = params

        @property
        def config_file(self) -> Mapping[str, str]:
            """

            :return: The parameters provided to it at construction
            """
            return self._params


class TestGaussmeterAddress(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.parameters["GAUSSMETER_ADDRESS"] = 'address'

    def test_gaussmeter_address(self):
        self.assertEqual(
            self.parameters["GAUSSMETER_ADDRESS"],
            self.loader.gaussmeter_address
        )


class TestLevelMeterAddress(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.parameters["LEVEL_METER_ADDRESS"] = "/dev/ttyUSB1"

    def test_level_meter_address(self):
        self.assertEqual(
            self.parameters["LEVEL_METER_ADDRESS"],
            self.loader.level_meter_address
        )


class TestLiquidHeliumChannel(OverloadedBootLoaderTestCase):
    def test_channel_not_int(self):
        channel = "Not a number"
        self.parameters["LIQUID_HELIUM_CHANNEL"] = channel

        self.assertRaises(
            BadConfigParameter, lambda: self.loader.liquid_helium_channel
        )

    def test_channel_not_allowed(self):
        channel = 113
        self.assertNotIn(
            channel,
            CryomagneticsLM510.ALLOWED_CHANNELS
        )
        self.parameters["LIQUID_HELIUM_CHANNEL"] = channel

        self.assertRaises(
            BadConfigParameter, lambda: self.loader.liquid_helium_channel
        )
