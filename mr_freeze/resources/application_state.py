# coding=utf-8
"""
Provides concrete implementations of the store and required variables
"""
from mr_freeze.resources.abstract_store import Store as _Store
from mr_freeze.resources.abstract_store import Variable as _Variable
from numpy import nan
from quantities import cm, gauss, A


class Store(_Store):
    """
    Contains a concrete implementation of the store to be used for
    manipulating data
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._variables = {
            LiquidHeliumLevel: LiquidHeliumLevel(nan * cm, self.executor),
            LiquidNitrogenLevel: LiquidNitrogenLevel(nan * cm, self.executor),
            MagneticField: MagneticField(nan * gauss, self.executor),
            Current: Current(nan * A, self.executor)
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