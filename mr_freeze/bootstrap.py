# -*- coding: utf-8 -*-
"""
Contains functions required to bootstrap the application
"""
import os
import logging
from configparser import ConfigParser
from typing import Optional
from mr_freeze.exceptions import NoConfigFileError

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
    def config_file(self) -> ConfigParser:
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
