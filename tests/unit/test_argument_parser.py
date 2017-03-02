import unittest
from mr_freeze.argument_parser import parser


class TestArgumentParser(unittest.TestCase):
    """
    Contains tests for the parser
    """
    def test_parsing(self):
        string_to_parse = "--gaussmeter-address=/dev/ttyUSB0"

        result = parser.parse_args([string_to_parse])
        self.assertIsNotNone(
            result.gaussmeter_address
        )
