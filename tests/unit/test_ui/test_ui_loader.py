# -*- coding: utf-8
"""
Contains unit tests for :mod:`mr_freeze.ui.ui_loader
"""
from mr_freeze.resources.application_state import LiquidHeliumLevel
from mr_freeze.resources.application_state import LiquidNitrogenLevel
from tests.unit.test_ui.user_interface_test_case import UserInterfaceTestCase
from quantities import cm
from numpy import nan


class TestLiquidHeliumLevelChange(UserInterfaceTestCase):
    def setUp(self):
        UserInterfaceTestCase.setUp(self)
        self.new_lhe_level = 3.0 * cm
        self.new_ln2_level = 3.0 * cm

    def test_lhe_variable_change(self):
        self.store[LiquidHeliumLevel].value = self.new_lhe_level

        self.assertEqual(
            float(self.new_lhe_level),
            self.ui.ui.liquid_helium_display.value()
        )

    def test_value_is_nan(self):
        self.store[LiquidHeliumLevel].value = nan
        self.assertIsNotNone(self.ui.ui.liquid_helium_display.value())

    def test_ln2_variable_change(self):
        self.store[LiquidNitrogenLevel].value = self.new_ln2_level

        self.assertEqual(
            float(self.new_ln2_level),
            self.ui.ui.liquid_nitrogen_display.value()
        )

