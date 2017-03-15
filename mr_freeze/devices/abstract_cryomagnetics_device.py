"""
Cryomagnetics does weird stuff with their device interfaces. This is where
the funky logic is captured
"""
import abc
import logging
import re
from instruments.abstract_instruments import Instrument as _Instrument
from threading import Lock
from mr_freeze.exceptions import NoEchoedCommandFoundError, NoResponseError

log = logging.getLogger(__name__)


class AbstractCryomagneticsDevice(_Instrument, metaclass=abc.ABCMeta):
    """
    Base class for devices that use Cryomagnetics instruments to
    communicate. The behaviour to query such a device over USB is special.

    A command is sent to the device, ending with ``\\r``. The command is
    then repeated back, ending with ``\\r\\n``. The response then follows,
    again ending with ``\\r\\n``. The trouble with this is that if I set
    ``\\r\\n`` as the terminator for the read response, then it is ambiguous
    when the message ends.

    To solve this problem, a maximum message size of 140 characters is
    defined in ``MAXIMUM_MESSAGE_SIZE``. It is assumed that this is enough
    space for the output of a single command.

    A querying lock in ``_querying_lock`` is also defined. This lock is
    acquired when querying and released after the response has been received.

    Queries are thread-safe.
    """
    _querying_lock = Lock()  # type: Lock

    MAXIMUM_MESSAGE_SIZE = 140

    def __init__(self, filelike):
        """
        Create an instance of this device

        :param filelike: The communicator to use for making calls to the device
        """
        super().__init__(filelike)

    @property
    def terminator(self):
        """

        :return: The termination character for the device
        """
        return '\r\n'

    def query(self, cmd, size=-1):
        """
        Write a command to the device, receive the response, and send this
        response to the parser.

        :param str cmd: The command to send
        :param int size: Ordinarily, this would represent the number of
            characters to read, but since this is fixed to
            ``MAXIMUM_MESSAGE_SIZE``, this parameter has no semantic
            meaning. It is here to provide a consistent API for using
            instruments.

        :return The response from the device
        :rtype: str
        """
        self._querying_lock.acquire()
        self.write(cmd + self.terminator)
        response = self.read(size=self.MAXIMUM_MESSAGE_SIZE)
        log.debug("received response %s", response)
        self._querying_lock.release()

        return self.parse_query(cmd, response)

    def parse_query(self, command, response):
        """
        After receiving the response from the device, extract the echoed
        command and the device response. Check that the echoed command
        matches the command sent to the device, and return the response

        :param command: The command which was sent to the device
        :param response: The response from the device
        :return: The response
        :rtype: str
        :raises: :exc:`RuntimeError` if the response or query cannot be
            retrieved
        """
        log.debug("Query parser received command %s and response %s",
                  command, response)

        echoed_command = re.search(
            r"^{0}(?={1})".format(command, self.terminator),
            response
        )
        response_from_device = re.search(
            r"(?<={0}).*(?={0}$)".format(self.terminator),
            response
        )

        log.debug(
            "Query parser parsed echoed command %s and response %s",
            echoed_command, response_from_device
        )

        if echoed_command is None:
            raise NoEchoedCommandFoundError(
                "Expected Command: {0} \n"
                "Device Response: {1}".format(command, response)
            )

        if response_from_device.group(0) is None:
            raise NoResponseError(
                "No response found in device response {0}".format(response)
            )

        return response_from_device.group(0)
