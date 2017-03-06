"""
Contains an abstract base class for all tasks that report a variable to the
CSV file. Each of these tasks also has a title field which states the title
of the variable
"""
import abc
from mr_freeze.tasks.abstract_task import AbstractTask


class ReportVariableTask(AbstractTask, metaclass=abc.ABCMeta):
    """
    The class describing how to report the variable
    """
    title = "Abstract Task"
