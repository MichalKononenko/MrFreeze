import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.resources.csv_file import CSVFile
from mr_freeze.tasks.write_csv_title import WriteCSVTitle


class TestWriteCSVTitle(unittest.TestCase):
    def setUp(self):
        self.csv_file = mock.MagicMock(spec=CSVFile)  # type: CSVFile
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.task = WriteCSVTitle(self.csv_file)


class TestWriteTitles(TestWriteCSVTitle):
    def test_write_titles(self):
        self.task.task(self.executor)
        self.assertTrue(
            self.csv_file.write_titles.called
        )
