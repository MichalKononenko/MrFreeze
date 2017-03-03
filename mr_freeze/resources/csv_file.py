import os
from typing import Iterable
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class CSVFile(object):
    """
    Represents an output of variables to CSV
    """
    _mode = 'ab'
    delimiter = ', '

    def __init__(
            self, path_to_csv_file: str, variables_to_write: Iterable[
                ReportVariableTask]
    ):
        self.path = path_to_csv_file
        self.variables = variables_to_write

        self._file_has_titles = False

    def write_titles(self):
        values_to_write = self.delimiter.join(
            [variable.title for variable in self.variables]
        ) + os.linesep

        with open(self.path, mode=self._mode) as file:
            file.write(values_to_write.encode())

    def write_values(self, values: Iterable):
        values_to_write = self.delimiter.join(
            [str(value) for value in values]
        ) + os.linesep
        with open(self.path, mode=self._mode) as file:
            file.write(values_to_write.encode())
