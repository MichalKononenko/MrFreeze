import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.devices.cryomagnetics_4g_adapter import Cryomagnetics4G
from mr_freeze.tasks.report_current import ReportCurrent


class TestReportCurrent(unittest.TestCase):
    gauge = mock.MagicMock(spec=Cryomagnetics4G)  # type: Cryomagnetics4G
    executor = mock.MagicMock(spec=Executor)  # type: Executor

    def setUp(self):
        self.task = ReportCurrent(gauge=self.gauge)


class TestInit(TestReportCurrent):
    def test_init(self):
        self.assertEqual(self.gauge, self.task.gauge)


class TestCall(TestReportCurrent):
    def test_call(self):
        self.task(self.executor)
        self.assertTrue(
            self.executor.submit.called
        )
        self.assertTrue(hasattr(self._task_function, '__call__'))

    def test_runtask(self):
        self.task(self.executor)
        current = self._task_function()
        self.assertEqual(self.gauge.current, current)

    @property
    def _task_function(self):
        return self.executor.submit.call_args[0][0]