"""
Contains unit tests for the Lakeshore 475 adapter
"""
import unittest
import unittest.mock as mock
import quantities as pq
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


class TestField(TestLakeshore475):

    class BadMagnetometer(object):
        @property
        def field(self):
            raise ValueError("Kaboom")

        @property
        def field_units(self):
            return pq.gauss

    def test_field_no_error(self):
        self.assertIsNotNone(self.instrument.field)

    def test_field_valueError(self):
        with mock.patch(
                'mr_freeze.devices.lakeshore_475.Lakeshore475.'
                '_magnetometer', new=self.BadMagnetometer()):
            field = self.instrument.field
        self.assertAlmostEqual(
            -100000.0 * pq.gauss, field
        )
