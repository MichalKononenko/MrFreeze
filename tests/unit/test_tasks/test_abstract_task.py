import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask


class ConcreteTask(AbstractTask):
    def task(self) -> int:
        return 1


class TestAbstractTask(unittest.TestCase):
    executor = mock.MagicMock(spec=Executor)

    def setUp(self):
        self.task = ConcreteTask()


class TestCall(TestAbstractTask):

    def test_submit(self):
        self.task(self.executor)

        self.assertTrue(self.executor.submit.called)
        self.assertEqual(
            mock.call(self.task.task),
            self.executor.submit.call_args
        )
