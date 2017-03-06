"""
Contains a task that asynchronously retrieves the current date. This task is
used to synchronize a series of measurements with one date, as well as
providing a single conceptual model for the application
"""
from concurrent.futures import Executor
from datetime import datetime
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class GetCurrentDate(ReportVariableTask):
    """
    Returns the date
    """
    title = "Date"

    def task(self, executor: Executor) -> str:
        """

        :param executor: The executor which will run this task
        :return: The current date, formatted into a string
        """
        return datetime.now().isoformat()
