import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.tasks.get_current_date import GetCurrentDate


class TestGetDate(unittest.TestCase):
    def setUp(self):
        self.task = GetCurrentDate()
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor

    def test_get_date(self):
        result = self.task.task(self.executor)
        self.assertIsInstance(result, str)
