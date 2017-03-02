"""
Contains unit tests for the Lakeshore 475 adapter
"""
import unittest
import unittest.mock as mock
from mr_freeze.devices.lakeshore_475 import Lakeshore475


class TestLakeshore475(unittest.TestCase):
    constructor = mock.MagicMock()

    def setUp(self):
        self.instrument = Lakeshore475()
        self.instrument._constructor = self.constructor

    def tearDown(self):
        self.constructor.reset_mock()


class TestPortName(TestLakeshore475):
    port = 'portName'

    def test_port_name(self):
        self.instrument.port_name = self.port
        self.assertEqual(
            self.port, self.instrument.port_name
        )


class TestAddress(TestLakeshore475):
    address = 1

    def test_address(self):
        self.instrument.address = self.address
        self.assertEqual(
            self.address, self.instrument.address
        )


class TestMagnetometer(TestLakeshore475):
    def test_no_construction_needed(self):
        _ = self.instrument._magnetometer
        self.assertTrue(
            self.constructor.open_gpibusb.called
        )

    def test_level_meter_no_construction(self):
        self.instrument._managed_instance = self.constructor
        self.assertEqual(self.constructor, self.instrument._magnetometer)
        self.assertFalse(self.constructor.open_gpibusb.called)
