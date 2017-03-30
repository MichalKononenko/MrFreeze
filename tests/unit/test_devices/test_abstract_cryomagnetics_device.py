# -*- coding: utf-8
"""
Contains unit tests for :mod:`mr_freeze.devices.abstract_cryomagnetics_device`
"""
import unittest
import unittest.mock as mock
from threading import Lock
from mr_freeze.devices.abstract_cryomagnetics_device import \
    AbstractCryomagneticsDevice


class ConcreteCryomagneticsDevice(AbstractCryomagneticsDevice):
    """
    Provides an implementation of a cryomagnetics device to test various
    methods
    """
    was_read_called = False
    data_to_read = None

    written_message = None
    was_write_called = False

    def __init__(self):
        self._querying_lock = mock.MagicMock(spec=Lock().__class__)
        self._filelike = mock.MagicMock()
        pass

    def read(self, *args, **kwargs):
        """
        Increment the read counter and return the data that is supposed to
        be "read" from the device
        """
        self.was_read_called = True
        return self.data_to_read

    def write(self, message):
        """
        Take the message to be written to a device and write it to an
        instance variable for later inspection
        """
        self.written_message = message
        self.was_write_called = True

    def reset(self):
        """
        Clear the messages sent to this device
        """
        self.was_read_called = False
        self.data_to_read = None
        self.written_message = None
        self.was_write_called = False


class TestAbstractCryomagneticsDevice(unittest.TestCase):
    def setUp(self):
        self.device = ConcreteCryomagneticsDevice()

    def tearDown(self):
        self.device.reset()


class TestQuery(TestAbstractCryomagneticsDevice):
    command = "enter"
    expected_response = "data"

    data_to_read = "%s\r\n%s\r\n" % (
        command, expected_response
    )

    def setUp(self):
        TestAbstractCryomagneticsDevice.setUp(self)
        self.device.data_to_read = self.data_to_read

    def test_query(self):
        self.assertEqual(
            self.expected_response,
            self.device.query(self.command)
        )
        self.assertTrue(
            self.device.was_write_called
        )
        self.assertTrue(
            self.device.was_read_called
        )


class TestParseQuery(TestAbstractCryomagneticsDevice):
    command = "Testing"
    data_format = "%s\r\n%s\r\n"

    def test_command_not_echoed_command(self):
        bad_echo = "String1"
        self.assertNotEqual(self.command, bad_echo)

        data_to_return = self.data_format % (bad_echo, "Response")

        with self.assertRaises(RuntimeError):
            self.device.parse_query(self.command, data_to_return)

    def test_command_bad_response(self):
        data_to_read = "%s%s" % (self.command, "response")

        with self.assertRaises(RuntimeError):
            self.device.parse_query(self.command, data_to_read)
