"""
Contains an implementation of the cryomagnetics LM 510 liquid cryogen level
monitor for InstrumentKit
"""
from mr_freeze.exceptions import InvalidChannelError, DataNotReadyError
from threading import Lock
from mr_freeze.devices.abstract_cryomagnetics_device \
    import AbstractCryomagneticsDevice
import quantities as pq
import re
import logging
from time import sleep

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CryomagneticsLM510(AbstractCryomagneticsDevice):
    """
    Represents a Cryomagnetics LM-510 liquid cryogen level monitor. Like all
    devices in InstrumentKit, the channels on this device are indexed starting
    from 0. Channel 1 is therefore 0, and Channel 2 is 1.
    """
    INSTRUMENT_TO_INDEX_CHANNELS = {
        1: 0,
        2: 1
    }
    INDEX_TO_INSTRUMENT_CHANNELS = {
        0: 1,
        1: 2
    }

    channel_measurement_lock = Lock()  # type: Lock
    querying_lock = Lock()  # type: Lock

    measurement_timeout = 0.5

    UNITS = {
        "cm": pq.cm,
        "in": pq.inch,
        "%": pq.percent,
        "percent": pq.percent
    }

    @property
    def default_channel(self):
        """
        The Level meter has a default channel that is used to measure
        different cryogen levels. If a channel is not specified for a
        particular command, the command gets sent to the value of the
        default channel instead

        :return: The current default channel
        :rtype: int
        """
        instrument_channel = int(self.query("CHAN?"))
        return self.INSTRUMENT_TO_INDEX_CHANNELS[instrument_channel]

    @default_channel.setter
    def default_channel(self, channel):
        """
        Set the default channel to the desired channel

        :param int channel: The desired channel
        :raises: :exc:`ValueError` if the channel to be set is not in the
        set of allowed channels defined in ``CHANNELS``
        """
        if channel not in self.INDEX_TO_INSTRUMENT_CHANNELS.keys():
            raise ValueError("Attempted to set channel to %s. Channel must "
                             "be an integer of either 1 or 2", channel)
        command = "CHAN %d" % self.INDEX_TO_INSTRUMENT_CHANNELS[channel]
        self.query(command)

    @property
    def status_byte(self):
        """
        Get a byte array representing the instrument's status byte. The
        status byte describes whether channel 1 or 2 are ready to make a
        measurement. The structure of the status byte is described in
        greater detail in the level meter's operating manual.

        :return: The current value of the status byte
        :rtype: bytes
        """
        byte_as_string = self.query("*STB?")
        return bytes([int(byte_as_string)])

    def reset(self):
        """
        Bring the instrument to a safe, known state
        """
        self.query("*RST")

    def __getitem__(self, channel):
        """

        Access a particular channel

        :param int channel: The index of the channel to access
        :return: An instance of the channel that can be used to obtain
            measurements
        """
        return self._Channel(channel, self)

    class _Channel(object):

        ALLOWED_CHANNEL_NUMBERS = {0, 1}

        _CHANNEL_NUMBER_TO_DATA_READY_BIT_INDEX = {
            0: 1,
            1: 4
        }

        def __init__(self, channel_number, instrument):
            self._check_channel(channel_number)

            self.instrument = instrument
            self.channel_number = channel_number

        @property
        def data_ready(self):
            """

            :return: ``True`` if the channel is ready, otherwise ``False``
            :rtype: bool
            """
            status_byte = self.instrument.status_byte
            return (int(status_byte[0]) &
                    self._CHANNEL_NUMBER_TO_DATA_READY_BIT_INDEX[
                        self.channel_number
                    ]) > 0

        @property
        def measurement(self):
            """

            Carry out a level measurement on the channel

            :return: The string returned from the level measurement
            :rtype: str
            """
            self.instrument.channel_measurement_lock.acquire()

            try:
                sleep(self.instrument.measurement_timeout)

                self._prepare_measurement()
                response = self.instrument.query(
                    "MEAS? %d" %
                    self.instrument.INDEX_TO_INSTRUMENT_CHANNELS[
                        self.channel_number
                    ]
                )
            finally:
                self.instrument.channel_measurement_lock.release()
            return self.parse_response(response)

        @staticmethod
        def parse_response(response):
            """
            Extract the value and unit in which the response was returned,
            and match these values to a physical quantity

            :param str response: The response returned by making a measurement
            :return: The measured quantity
            :rtype: Quantity
            """
            value_match = re.search("^(\d|\.)*(?=\s)", response)
            unit_match = re.search("(?<=\s).*(?=$)", response)

            value = float(value_match.group(0))
            unit = CryomagneticsLM510.UNITS[unit_match.group(0)]

            return_value = value * unit

            log.debug("parsed quantity %s from response %s", return_value,
                      response)
            return return_value

        def _check_channel(self, channel):
            """

            :param channel: The channel to check
            :raises: ``InvalidChannelError`` if the channel is not allowed
            """
            if channel not in self.ALLOWED_CHANNEL_NUMBERS:
                raise InvalidChannelError(
                    "Tried to set channel to {0}. Allowed channels are {1}".\
                    format(
                        channel, self.instrument.ALLOWED_CHANNEL_NUMBERS
                    )
                )

        def _prepare_measurement(self):
            response = self.instrument.query("MEAS {0}".format(
                self.channel_number
            ))

            sleep(self.instrument.measurement_timeout)

            if not self.data_ready:
                raise DataNotReadyError(
                    "Data not ready. Received response {0}".format(response))

            assert self.data_ready
