import os
import unittest
import unittest.mock as mock
from mr_freeze.tasks.report_variable_task import ReportVariableTask
from mr_freeze.resources.csv_file import CSVFile

TESTING_PARAMETERS = {
    "file-name": os.path.join(os.curdir, 'test.csv')
}


class TestCSVFile(unittest.TestCase):
    mock_variable_1 = mock.MagicMock(spec=ReportVariableTask)
    mock_variable_1.title = "Variable 1"

    mock_variable_2 = mock.MagicMock(spec=ReportVariableTask)
    mock_variable_2.title = "Variable 2"

    def setUp(self):
        self.variables = (self.mock_variable_1, self.mock_variable_2)

        self.file = CSVFile(TESTING_PARAMETERS["file-name"], self.variables)

    @staticmethod
    def read_csv_file():
        with open(TESTING_PARAMETERS["file-name"], mode='rb') as file:
            return os.linesep.join({line.decode() for line in file})

    def tearDown(self):
        if os.path.exists(TESTING_PARAMETERS["file-name"]):
            os.remove(TESTING_PARAMETERS["file-name"])


class TestWriteTitles(TestCSVFile):
    def test_write_titles(self):
        self.file.write_titles()
        written_data = self.read_csv_file()

        self.assertEqual(
            self.expected_data,
            written_data
        )

    @property
    def expected_data(self):
        return self.file.delimiter.join(
            {variable.title for variable in self.variables}
        ) + os.linesep


class TestWriteValues(TestCSVFile):
    def setUp(self):
        TestCSVFile.setUp(self)
        self.values = (1, 2, 3)

    def test_write_values(self):
        self.file.write_values(self.values)
        written_data = self.read_csv_file()

        self.assertEqual(
            self.expected_data,
            written_data
        )

    @property
    def expected_data(self):
        return self.file.delimiter.join(
            {str(value) for value in self.values}
        ) + os.linesep
