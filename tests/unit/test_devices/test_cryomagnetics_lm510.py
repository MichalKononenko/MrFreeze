"""
Contains unit tests for static methods in the LM510 implementation that can
be effectively unit tested
"""
import unittest
from mr_freeze.devices.cryomagnetics_lm510 import CryomagneticsLM510
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
        ("15.0 CM", 15.0 * pq.cm),
        ("25.3 IN", 25.3 * pq.inch),
        ("123.7 %", 123.7 * pq.percent),
        ("4.9 PERCENT", 4.9 * pq.percent)
    )

    def test_parser(self):
        """
        Loop through the parameters defined above and ensure that they pass
        """
        for parameter in self.test_parameters:
            self._run_test(parameter)

    def _run_test(self, parameter):
        self.assertEqual(
            parameter[1],
            CryomagneticsLM510.parse_response(parameter[0])
        )


class TestParseQuery(TestCryomagneticsLM510):
    """
    Contains unit tests for the query parser
    """
    test_parameters = (
        ("*IDN?\r\n", "*IDN?\r\nData", "Data"),
    )

    def test_parser(self):
        """
        Loop through the parameters and ensure they pass
        """
        for parameter in self.test_parameters:
            self._run_test(parameter)

    def _run_test(self, parameter):
        self.assertEqual(
            parameter[2],
            CryomagneticsLM510.parse_query(
                parameter[0], parameter[1]
            )
        )