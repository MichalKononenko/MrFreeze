# coding=utf-8
"""
Manages a cache of the last measured variable. Capable of notifying other
resources that a variable changed
"""
from typing import TypeVar, Callable, Set
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

    def __init__(
            self,
            initial_value: V,
            variable_update_executor: Executor
    ) -> None:
        self._value = initial_value
        self._listeners = self._ListenerSet()  # type: Set[Callable[[V], None]
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
    def listeners(self) -> Set[Callable[[V], None]]:
        """

        :return: The list of callbacks that are listening for changes to
         this variable
        """
        return self._listeners

    def _notify_listeners(self):
        """
        Notify the active listeners that the value of the variable changed
        """
        for listener_ref in self.listeners:
            meth = listener_ref()
            if meth is not None:
                self._executor.submit(meth, self._value)

    def __repr__(self):
        return "%s(initial_value=%s)" % (
            self.__class__.__name__, self._value
        )

    class _ListenerSet(Set):
        """
        Contains the listeners
        """
        def __init__(self):
            super(Set, self).__init__()
            self.listeners = set()

        def add(self, listener: Callable[[V], None]) -> None:
            """
            Add a weak reference to the listener in the set.
            The ``hasattr(__self__)`` test is used to check whether the
            method is bound or not. If the listener to add is a bound
            method, a ``WeakMethod`` is stored instead of a generic weak
            reference. This has to be done because bound methods in Python
            are garbage-collected differently than conventional methods.
            """
            if self._is_bound_method(listener):
                ref = weakref.WeakMethod(listener)
            else:
                ref = weakref.ref(listener)
            self.listeners.add(ref)

        @staticmethod
        def _is_bound_method(method: Callable[[V], None]) -> bool:
            return hasattr(method, '__self__')

        def __iter__(self):
            """

            :return: The iterator of the underlying set of listeners that this
            set is managing
            """
            return self.listeners.__iter__()


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
