# -*- coding: utf-8 -*-
"""
Contains unit tests for the bootloader
"""
import unittest
import unittest.mock as mock
import os
from typing import Mapping
from mr_freeze.bootstrap import BootLoader
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

    def test_channel(self):
        channel = 1
        self.parameters["LIQUID_HELIUM_CHANNEL"] = channel

        self.assertEqual(
            channel, self.loader.liquid_helium_channel
        )


class TestLiquidNitrogenChannel(OverloadedBootLoaderTestCase):
    def test_channel_not_int(self):
        channel = "Not a number"
        self.parameters["LIQUID_NITROGEN_CHANNEL"] = channel
        self.assertRaises(
            BadConfigParameter, lambda: self.loader.liquid_nitrogen_channel
        )

    def test_channel_not_allowed(self):
        channel = 113
        self.assertNotIn(
            channel,
            CryomagneticsLM510.ALLOWED_CHANNELS
        )
        self.parameters["LIQUID_NITROGEN_CHANNEL"] = channel
        self.assertRaises(
            BadConfigParameter,
            lambda: self.loader.liquid_nitrogen_channel
        )


class TestPowerSupplyAddress(OverloadedBootLoaderTestCase):
    def test_power_supply_address(self):
        address = "foo"
        self.parameters["POWER_SUPPLY_ADDRESS"] = address
        self.assertEqual(
            address, self.loader.power_supply_address
        )


class TestCSVOutputDirectory(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.bad_directory = 'dsgjkshje'
        self.good_directory = os.path.abspath(os.curdir)
        self.assertFalse(os.path.isdir(self.bad_directory))

    def test_bad_directory(self):
        self.parameters["CSV_OUTPUT_DIRECTORY"] = self.bad_directory

        self.assertRaises(
            BadConfigParameter,
            lambda: self.loader.csv_output_directory
        )

    def test_good_directory(self):
        self.parameters["CSV_OUTPUT_DIRECTORY"] = self.good_directory

        self.assertEqual(
            self.good_directory,
            self.loader.csv_output_directory
        )


class TestPipeOutputFile(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.bad_directory = 'askjfkaljrwa'

        self.bad_file = os.path.join(self.bad_directory, 'pipe.json')
        self.good_file = os.path.abspath(
            os.path.join(os.curdir, 'pipe.json')
        )

        self.assertFalse(os.path.isdir(self.bad_directory))

    def test_bad_directory(self):
        self.parameters["PIPE_OUTPUT_FILE"] = self.bad_file

        self.assertRaises(
            BadConfigParameter,
            lambda: self.loader.pipe_output_file
        )

    def test_good_directory(self):
        self.parameters["PIPE_OUTPUT_FILE"] = self.good_file

        self.assertEqual(
            self.good_file,
            self.loader.pipe_output_file
        )


class TestSampleInterval(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.good_interval = 900
        self.bad_interval = "not an int"

    def test_good_interval(self):
        self.parameters["SAMPLE_INTERVAL"] = str(self.good_interval)
        self.assertEqual(
            self.good_interval,
            self.loader.sample_interval
        )

    def test_bad_interval(self):
        self.parameters["SAMPLE_INTERVAL"] = self.bad_interval
        self.assertRaises(
            BadConfigParameter,
            lambda: self.loader.sample_interval
        )


class TestTaskTimeout(OverloadedBootLoaderTestCase):
    def setUp(self):
        OverloadedBootLoaderTestCase.setUp(self)
        self.bad_timeout = "not an int"
        self.good_timeout = 900

    def test_good_interval(self):
        self.parameters["TASK_TIMEOUT"] = str(self.good_timeout)
        self.assertEqual(
            self.good_timeout,
            self.loader.task_timeout
        )

    def test_bad_interval(self):
        self.parameters["TASK_TIMEOUT"] = self.bad_timeout
        self.assertRaises(
            BadConfigParameter,
            lambda: self.loader.task_timeout
        )
