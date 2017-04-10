# coding=utf-8
"""
Manages a cache of the last measured variable. Capable of notifying other
resources that a variable changed
"""
from typing import NewType, TypeVar, Callable, Set
from concurrent.futures import Executor
import weakref
import abc
from six import add_metaclass

V = TypeVar("V")


@add_metaclass(abc.ABCMeta)
class Variable(object):
    """
    Capable of notifying on change
    """
    ListenerType = NewType("ListenerType", Callable[[V], None])

    def __init__(
            self,
            initial_value: V,
            variable_update_executor: Executor
    ) -> None:
        self._value = initial_value
        self._listeners = weakref.WeakSet()  # type: Set[Callable[V]]
        self._executor = variable_update_executor

    @property
    def value(self) -> V:
        """

        :return: The current value
        """
        return self._value

    @value.setter
    def value(self, new_value: V):
        """

        :param new_value: The new value of the variable
        :return:
        """
        self._value = new_value
        self._notify_listeners()

    @property
    def listeners(self) -> Set[ListenerType]:
        """

        :return: The list of callbacks that are listening for changes to
         this variable
        """
        return self._listeners

    def _notify_listeners(self):
        """
        Notify the active listeners that the value of the variable changed
        """
        for listener in self.listeners:
            if listener is not None:
                self._executor.submit(listener, self._value)

    def __repr__(self):
        return "%s(initial_value=%s)" % (
            self.__class__.__name__, self._value
        )


@add_metaclass(abc.ABCMeta)
class Store(object):
    """
    Contains variables
    """
    EXECUTOR_MAX_WORKERS = 5

    def __init__(self, variable_update_executor: Executor) -> None:
        self.executor = variable_update_executor
        self._variables = {}

    def __getitem__(self, item: Variable.__class__) -> Variable:
        """

        :param item:
        :return:
        """
        return self._variables[item]

    def __repr__(self):
        return "%s(variable_update_executor=%s)" % (
            self.__class__.__name__, self.executor
        )
