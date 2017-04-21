# coding=utf-8
"""
Provides concrete implementations of the store and required variables
"""
import os
from concurrent.futures import Executor
from mr_freeze.resources.abstract_store import Store as _Store
from mr_freeze.resources.abstract_store import Variable as _Variable
from numpy import nan
from quantities import cm, gauss, A


class Store(_Store):
    """
    Contains a concrete implementation of the store to be used for
    manipulating data
    """
    def __init__(self, variable_update_executor: Executor) -> None:
        super(self.__class__, self).__init__(variable_update_executor)
        self._variables = {
            LiquidHeliumLevel: LiquidHeliumLevel(nan * cm, self.executor),
            LiquidNitrogenLevel: LiquidNitrogenLevel(nan * cm, self.executor),
            MagneticField: MagneticField(nan * gauss, self.executor),
            Current: Current(nan * A, self.executor),
            LoggingInterval: LoggingInterval(15, self.executor),
            UpperSweepCurrent: UpperSweepCurrent(0.5, self.executor),
            LowerSweepCurrent: LowerSweepCurrent(0.5, self.executor),
            PowerSupply: PowerSupply(None, self.executor),
            CSVDirectory: CSVDirectory(os.devnull, self.executor)
        }


class LiquidHeliumLevel(_Variable):
    """
    Describes the level of liquid helium
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class LiquidNitrogenLevel(_Variable):
    """
    Describes the level of liquid nitrogen
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class MagneticField(_Variable):
    """
    Describes the magnetic field present in the substance
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class Current(_Variable):
    """
    Describes the current going into the power supply
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class LoggingInterval(_Variable):
    """
    Describes the amount of time that should elapse before logging
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class CSVDirectory(_Variable):
    """
    Describes where to write the logfile
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class UpperSweepCurrent(_Variable):
    """
    The upper sweep current
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class LowerSweepCurrent(_Variable):
    """
    The lower sweep current
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)


class PowerSupply(_Variable):
    """
    The power supply instrument
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
