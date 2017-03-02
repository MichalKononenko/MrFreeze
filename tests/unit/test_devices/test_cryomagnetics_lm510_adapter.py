"""
Contains unit tests for the Cryomagnetics LM510 adapter
"""
import unittest
import unittest.mock as mock
from mr_freeze.devices.cryomagnetics_lm510_adapter import CryomagneticsLM510


class TestAdapter(unittest.TestCase):
    """
    Base class for unit tests of the adapter layer
    """
    constructor = mock.MagicMock()

    def setUp(self):
        self.instrument = CryomagneticsLM510()
        self.instrument._constructor = self.constructor

    def tearDown(self):
        self.constructor.reset_mock()


class TestPortName(TestAdapter):
    port = 'portName'

    def test_port_name(self):
        self.instrument.port_name = self.port
        self.assertEqual(
            self.port, self.instrument.port_name
        )


class TestBaudRate(TestAdapter):
    baud = 19200

    def test_baud(self):
        self.instrument.baud_rate = self.baud

        self.assertEqual(
            self.baud, self.instrument.baud_rate
        )


class TestTimeoutInSeconds(TestAdapter):
    timeout = 1

    def test_timeout(self):
        self.instrument.timeout_in_seconds = self.timeout
        self.assertEqual(
            self.timeout, self.instrument.timeout_in_seconds
        )


class TestLevelMeter(TestAdapter):
    def test_level_meter_construction_required(self):
        _ = self.instrument._level_meter
        self.assertTrue(self.constructor.open_serial.called)

    def test_level_meter_no_construction(self):
        self.instrument._managed_instance = self.constructor
        self.assertEqual(self.constructor, self.instrument._level_meter)
        self.assertFalse(self.constructor.open_serial.called)
