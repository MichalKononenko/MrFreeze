"""
Cryomagnetics does weird stuff with their device interfaces. This is where
the funky logic is captured
"""
import abc
import logging
import re
from instruments.abstract_instruments import Instrument as _Instrument
from threading import Lock

log = logging.getLogger(__name__)


class AbstractCryomagneticsDevice(_Instrument, metaclass=abc.ABCMeta):
    _querying_lock = Lock()  # type: Lock

    def __init__(self, filelike):
        super().__init__(filelike)

    def query(self, cmd, size=-1):
        self._querying_lock.acquire()
        self.terminator = '\r\n'
        self.write(cmd + self.terminator)
        self.terminator = '\r\n\n'

        response = self.read(size=size)
        log.debug("received response %s", response)
        self._querying_lock.release()

        return self.parse_query(cmd, response)

    @staticmethod
    def parse_query(command, response):
        log.debug("Query parser received command %s and response %s",
                  command, response)

        echoed_command = re.search("^.*(?=\r\n)", response)
        response_from_device = re.search(
            "(?<=\r\n).*(?=\r\n\n$)",
            response
        )

        log.debug(
            "Query parser parsed echoed command %s and response %s",
            echoed_command, response_from_device
        )

        if (echoed_command is None) or (response_from_device is None):
            raise RuntimeError(
                "Cryomagnetics query parser did not match search string"
            )

        if command != echoed_command.group(0):
            raise RuntimeError(
                "Cryomagnetics query parser did not find echoed command"
            )

        if response_from_device.group(0) is None:
            raise RuntimeError(
                "I/O with Cryomagnetics instrument did not return a response"
            )

        return response_from_device.group(0)