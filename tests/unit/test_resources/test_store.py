# coding=utf-8
"""
Contains unit tests for :mod:`mr_freeze.resources.store`
"""
import unittest
import unittest.mock as mock
from concurrent.futures import Executor
from mr_freeze.resources.abstract_store import Store, Variable


class PressureVariable(Variable):
    """
    Describes the measured pressure
    """


class PressureStore(Store):
    """
    A store containing the pressure
    """
    def __init__(self, executor, variable):
        super(self.__class__, self).__init__(executor)
        self._variables = {
            PressureVariable: variable
        }


class TestVariable(unittest.TestCase):
    """
    Contains unit tests for the variable
    """
    def setUp(self):
        self.initial_value = 3.0
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.variable = PressureVariable(self.initial_value, self.executor)
        self.listener = mock.MagicMock()


class TestValue(TestVariable):
    def test_value(self):
        self.assertAlmostEqual(self.initial_value, self.variable.value)

    def test_setter(self):
        self.variable._notify_listeners = mock.MagicMock()
        self.variable.value = 4.0

        self.assertTrue(
            self.variable._notify_listeners.called
        )


class TestListeners(TestVariable):
    def setUp(self):
        TestVariable.setUp(self)
        self.variable.listeners.add(self.listener)
        self.new_value = 5.0

    def test_setter(self):
        self.variable.value = self.new_value

        self.assertEqual(
            mock.call(self.listener, self.new_value),
            self.executor.submit.call_args
        )


class TestStore(unittest.TestCase):
    """
    Base class for testing the store
    """
    def setUp(self):
        self.executor = mock.MagicMock(spec=Executor)  # type: Executor
        self.variable = mock.MagicMock(spec=PressureVariable)
        self.store = PressureStore(self.executor, self.variable)


class TestGetItem(TestStore):
    def setUp(self):
        TestStore.setUp(self)

    def test_getitem(self):
        self.assertEqual(
            self.variable, self.store[self.variable.__class__]
        )
