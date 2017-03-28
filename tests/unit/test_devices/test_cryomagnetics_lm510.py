# -*- coding: utf-8 -*-
"""
Contains unit tests for static methods in the LM510 implementation that can
be effectively unit tested
"""
import unittest
import unittest.mock as mock
from mr_freeze.devices.cryomagnetics_lm510 import CryomagneticsLM510
from threading import Lock
import quantities as pq


class TestCryomagneticsLM510(unittest.TestCase):
    """
    Base class for the test
    """
    pass


class TestParseResponse(TestCryomagneticsLM510):
    """
    Contains unit tests for the response parser
    """
    test_parameters = (
        ("15.0 cm", 15.0 * pq.cm),
        ("25.3 in", 25.3 * pq.inch),
        ("123.7 %", 123.7 * pq.percent),
        ("4.9 percent", 4.9 * pq.percent)
    )

    def test_parser(self):
        """
        Loop through the parameters defined above and ensure that they pass
        """
        for parameter in self.test_parameters:
            self._run_test(parameter)

    def _run_test(self, parameter: tuple):
        """

        :param parameter: The parameter for which the test is to be run
        """
        self.assertEqual(
            parameter[1],
            CryomagneticsLM510._Channel.parse_response(parameter[0])
        )


class TestGetItem(TestCryomagneticsLM510):
    def setUp(self):
        self.instrument = CryomagneticsLM510.open_test()

    def test_getItem_allowed(self):
        allowed_channel = 0
        channel = self.instrument[allowed_channel]

        self.assertIsInstance(channel, self.instrument._Channel)


class TestMeasurementDeadlockManagement(TestCryomagneticsLM510):
    """
    Found during a debugging session, this test attempts to replicate a
    condition where the measurement preparation method fails while the
    device's channel measurement lock is acquired.
    """
    def setUp(self):
        TestCryomagneticsLM510.setUp(self)
        self.channel = 0

        self.instrument = CryomagneticsLM510.open_test()

        self.instrument.channel_measurement_lock = mock.MagicMock(
            spec=Lock().__class__
        )
        self.instrument.query = mock.MagicMock(return_value="10 A")

    def test_deadlock_management(self):
        with mock.patch(
                'mr_freeze.devices.cryomagnetics_lm510.CryomagneticsLM510.'
                '_Channel._prepare_measurement',
                side_effect=Exception("Something was thrown")
        ) as mock_method:
            self.assertRaises(
                Exception, lambda: self.instrument[0].measurement
            )

        self.assertTrue(mock_method.called)
        self.assertTrue(
             self.instrument.channel_measurement_lock.acquire.called
        )
        self.assertTrue(
            self.instrument.channel_measurement_lock.release.called
        )