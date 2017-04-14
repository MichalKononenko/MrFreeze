# coding=utf-8
"""
Contains unit tests for updating the store
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from quantities import cm, A, gauss
from mr_freeze.resources.abstract_store import Store
from mr_freeze.resources.application_state import Store as ConcreteStore
from mr_freeze.tasks.update_store import UpdateStore
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.resources.application_state import Current


class TestUpdateStore(unittest.TestCase):
    """
    Base unit test
    """
    def setUp(self):
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.store = ConcreteStore(self.executor)  # type: Store
        self.new_lhe_level = 3.0 * cm
        self.new_ln2_level = 10.0 * cm
        self.new_current = 50.0 * A
        self.magnetic_field = 1e4 * gauss

        self.task = UpdateStore(
            self.store,
            self.new_lhe_level,
            self.new_ln2_level,
            self.new_current,
            self.magnetic_field
        )


class TestTask(TestUpdateStore):
    """
    Contains tests for the task
    """
    def test_task(self):
        self.task.task(self.executor)

        self.assertEqual(
            self.new_lhe_level, self.store[LiquidHeliumLevel].value
        )
