from concurrent.futures import Executor
from datetime import datetime
from mr_freeze.tasks.report_variable_task import ReportVariableTask


class GetCurrentDate(ReportVariableTask):
    title = "Date"

    def task(self, executor: Executor):
        return str(datetime.now())
