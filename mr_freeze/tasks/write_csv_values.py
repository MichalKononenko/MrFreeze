from typing import Tuple
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.csv_file import CSVFile


class WriteCSVValues(AbstractTask):
    def __init__(self, file: CSVFile, values_to_write: Tuple):
        self.values = values_to_write
        self.file = file

    def task(self):
        self.file.write_values(self.values)
