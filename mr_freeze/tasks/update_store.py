# coding=utf-8
"""
Describes a task for updating the application state during execution
"""
from concurrent.futures import Executor
from mr_freeze.tasks.abstract_task import AbstractTask
from mr_freeze.resources.abstract_store import Store, Variable
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from mr_freeze.resources.application_state import MagneticField
from mr_freeze.resources.application_state import Current
from quantities import Quantity


class UpdateStore(AbstractTask):
    """
    Update the application state with these new values
    """
    def __init__(self, store: Store,
                 new_lhe_level: Quantity=None,
                 new_ln2_level: Quantity=None,
                 new_current: Quantity=None,
                 new_magnetic_field: Quantity=None) -> None:
        super(self.__class__, self).__init__()
        self.store = store
        self.new_lhe_level = new_lhe_level

        self.variables = {
            LiquidHeliumLevel: new_lhe_level,
            LiquidNitrogenLevel: new_ln2_level,
            Current: new_current,
            MagneticField: new_magnetic_field
        }

    def task(self, executor: Executor) -> None:
        """
        Run the task

        :param executor: The executor to use
        """
        for key in self.variables.keys():
            self._update_variable(key, self.variables[key], self.store)

    @staticmethod
    def _update_variable(
            variable: Variable, value: Quantity, store: Store) -> None:
        """
        Update the variable if the variable is not None

        :param Variable variable: The variable to update
        :param store:
        :return:
        """
        if variable is not None:
            store[variable] = value
