# -*- coding: utf-8 -*-
"""
Contains the user-defined exceptions that this application will throw if
something goes wrong
"""


class NoConfigFileError(FileNotFoundError, IOError):
    """
    Thrown if a configuration file is not found
    """
    pass


class BadConfigParameter(ValueError):
    """
    Thrown if a configuration parameter was not correctly set
    """
    pass


class DeviceCommunicationError(RuntimeError, IOError):
    """
    Thrown if a query could not be answered
    """
    pass


class NoEchoedCommandFoundError(DeviceCommunicationError):
    """
    Thrown if the echoed command regex did not find an echoed command
    """
    pass


class NoResponseError(DeviceCommunicationError):
    """
    Thrown if no response to the command was found in the echo of the device
    """
    pass


class DataNotReadyError(DeviceCommunicationError):
    """
    Thrown if data that should be ready is not
    """
    pass


class InvalidChannelError(ValueError):
    """
    Thrown if trying to access a channel that does not exist on an instrument
    """
    pass
