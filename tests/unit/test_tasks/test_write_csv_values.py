import unittest
import unittest.mock as mock
from mr_freeze.resources.csv_file import CSVFile
from mr_freeze.tasks.write_csv_values import WriteCSVValues


class TestWriteCSVValues(unittest.TestCase):
    mock_variable_1 = mock.MagicMock()
    mock_variable_2 = mock.MagicMock()

    def setUp(self):
        self.csv_file = mock.MagicMock(spec=CSVFile)  # type: CSVFile
        self.values = (self.mock_variable_1, self.mock_variable_2)

        self.task = WriteCSVValues(self.csv_file, self.values)


class TestWriteValues(TestWriteCSVValues):
    def test_task(self):
        self.task.task()
        self.assertEqual(
            mock.call(self.values),
            self.csv_file.write_values.call_args
        )
