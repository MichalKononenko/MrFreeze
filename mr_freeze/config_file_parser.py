# -*- coding: utf-8 -*-
"""
Contains functions required to bootstrap the application
"""
import os
import logging
from configparser import ConfigParser
from typing import Optional, Mapping
from mr_freeze.exceptions import NoConfigFileError, BadConfigParameter
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510
from mr_freeze import APPLICATION_DIRECTORY

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ConfigFileParser(object):
    """
    Describes the bootloader for the application
    """
    _root_directory = os.path.abspath(os.path.sep)

    CONFIG_FILE_LOCATIONS = (
        os.path.join(_root_directory, "etc", "mr-freeze.conf"),
        os.path.join(os.path.curdir, "mr-freeze.conf"),
        os.path.join(APPLICATION_DIRECTORY, "mr-freeze.conf")
    )

    _CONFIG_SECTION_KEY = "Mr-Freeze"
    _GAUSSMETER_ADDRESS_KEY = "GAUSSMETER_ADDRESS"
    _LEVEL_METER_GAUGE_KEY = "LEVEL_METER_ADDRESS"
    _LIQUID_HELIUM_CHANNEL_KEY = "LIQUID_HELIUM_CHANNEL"
    _LIQUID_NITROGEN_CHANNEL_KEY = "LIQUID_NITROGEN_CHANNEL"
    _POWER_SUPPLY_ADDRESS_KEY = "POWER_SUPPLY_ADDRESS"
    _CSV_OUTPUT_DIRECTORY_KEY = "CSV_OUTPUT_DIRECTORY"
    _PIPE_OUTPUT_FILE_KEY = "PIPE_OUTPUT_FILE"
    _SAMPLE_INTERVAL_KEY = "SAMPLE_INTERVAL"
    _TASK_TIMEOUT_KEY = "TASK_TIMEOUT"

    def __init__(self) -> None:
        self._config_file_parser = ConfigParser()
        self._last_config_file_read = None

    @property
    def config_file_name(self) -> Optional[str]:
        """
        First, look for a file ``/etc/mr-freeze.conf``. If this file does
        not exist, look for ``mr-freeze.conf`` in this directory.

        :return: The name of the configuration file, or None if there is no
        config file
        """
        for path in self.CONFIG_FILE_LOCATIONS:
            if os.path.isfile(path):
                return path
        return None

    @property
    def config_file(self) -> Mapping[str, str]:
        """

        :return: A parsed configuration file
        :raises: :exc:`NoConfigFileError` if the configuration file doesn't
            exist
        """
        file = self.config_file_name

        if file is None:
            raise NoConfigFileError("No configuration file was found")

        if file != self._last_config_file_read:
            self._config_file_parser.read(file)

        self._last_config_file_read = file

        return self._config_file_parser[self._CONFIG_SECTION_KEY]

    @property
    def gaussmeter_address(self) -> str:
        """

        :return: The address of the gaussmeter as written in the
        """
        return self.config_file[self._GAUSSMETER_ADDRESS_KEY]

    @property
    def level_meter_address(self) -> str:
        """

        :return: The address of the level meter
        """
        return self.config_file[self._LEVEL_METER_GAUGE_KEY]

    @property
    def liquid_helium_channel(self) -> int:
        """

        :return: The channel on which liquid helium is located
        """
        from_file = self.config_file[self._LIQUID_HELIUM_CHANNEL_KEY]

        try:
            channel_number = int(from_file)
        except ValueError:
            raise BadConfigParameter(
                "The value %s read from config is not an integer" %
                from_file
            )

        if channel_number not in \
                CryomagneticsLM510.INDEX_TO_INSTRUMENT_CHANNELS.keys():
            raise BadConfigParameter(
                "The channel number %d is not a valid channel in %s" %
                (channel_number,
                 CryomagneticsLM510.INDEX_TO_INSTRUMENT_CHANNELS.keys())
            )

        return channel_number

    @property
    def liquid_nitrogen_channel(self) -> int:
        """

        :return: The channel on which liquid nitrogen level is measured
        """
        from_file = self.config_file[self._LIQUID_NITROGEN_CHANNEL_KEY]

        try:
            channel = int(from_file)
        except ValueError:
            raise BadConfigParameter(
                "The value %s read from config is not an integer",
                from_file
            )

        if channel not in CryomagneticsLM510.ALLOWED_CHANNELS:
            raise BadConfigParameter(
                "The channel number %d is not a valid channel for %s" %
                (channel, CryomagneticsLM510)
            )

        return channel

    @property
    def power_supply_address(self) -> str:
        """

        :return: The address of the power supply
        """
        return self.config_file[self._POWER_SUPPLY_ADDRESS_KEY]

    @property
    def csv_output_directory(self) -> str:
        """

        :return: The directory to which the CSV file is to be written
        """
        from_file = self.config_file[self._CSV_OUTPUT_DIRECTORY_KEY]

        if not os.path.isdir(from_file):
            raise BadConfigParameter(
                "The file %s is not a directory" % from_file
            )

        return from_file

    @property
    def pipe_output_file(self) -> str:
        """

        :return: The directory where ``pipe.json`` is to be written
        """
        from_file = self.config_file[self._PIPE_OUTPUT_FILE_KEY]

        if not os.path.isdir(os.path.split(from_file)[0]):
            raise BadConfigParameter(
                "The directory %s was not found" % from_file
            )

        return from_file

    @property
    def sample_interval(self) -> int:
        """

        :return: The amount of time required before running samples
        """
        from_file = self.config_file[self._SAMPLE_INTERVAL_KEY]

        try:
            return int(from_file)
        except ValueError:
            raise BadConfigParameter(
                "The parameter %s for sample interval could not be"
                "converted to an integer" % from_file
            )

    @property
    def task_timeout(self) -> int:
        """

        :return: The time that should elapse before a task is considered dead
        """
        from_file = self.config_file[self._TASK_TIMEOUT_KEY]
        try:
            return int(from_file)
        except ValueError:
            raise BadConfigParameter(
                "The parameter %s for sample interval could not be"
                "converted to an integer" % from_file
            )
