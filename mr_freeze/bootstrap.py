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

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class BootLoader(object):
    """
    Describes the bootloader for the application
    """
    CONFIG_FILE_LOCATIONS = (
        os.path.join("etc", "mr-freeze.conf"),
        os.path.join(os.path.curdir, "mr-freeze.conf")
    )

    _GAUSSMETER_ADDRESS_KEY = "GAUSSMETER_ADDRESS"
    _LEVEL_METER_GAUGE_KEY = "LEVEL_METER_ADDRESS"
    _LIQUID_HELIUM_CHANNEL_KEY = "LIQUID_HELIUM_CHANNEL"

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

        return self._config_file_parser

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
