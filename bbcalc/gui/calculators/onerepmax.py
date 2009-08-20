## -*- coding: utf-8 -*-

import gconf

from kiwi.ui.delegates import SlaveDelegate

import bbcalc.utils.config as config

from bbcalc.calculators.onerepmax import onerep_max_calc

from bbcalc.utils import METRIC, IMPERIAL
from bbcalc.utils.unitconvertor import convert_mass

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (220.0, 100.0)


class OneRepMax(SlaveDelegate):
    gladefile = 'one_rep_max_window'

    def __init__(self):
        SlaveDelegate.__init__(self)

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()
        # Set active item for unit selection box
        self.unit_combobox.set_active(self.config.measurement_system)
        # Set default value(s)
        self.weight_spinbutton.set_value(DEFAULT_WEIGHT[self.config.measurement_system])

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)

    # Signal handlers

    def after_unit_combobox__changed(self, entry, *args):
        active = entry.get_active()
        weight = self.weight_spinbutton.get_value()
        self.weight_spinbutton.set_value(convert_mass(weight, active))

    # TODO: Re-factore this methods
    def after_weight_spinbutton__changed(self, entry, *args):
        # Result calculation
        weight = self.weight_spinbutton.get_value()
        reps = self.reps_spinbutton.get_value()

        self.result_entry.set_text(str(onerep_max_calc(weight, int(reps))))

    def after_reps_spinbutton__changed(self, entry, *args):
        # Result calculation
        weight = self.weight_spinbutton.get_value()
        reps = self.reps_spinbutton.get_value()

        self.result_entry.set_text(str(onerep_max_calc(weight, int(reps))))

    def on_gconf_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit_combobox.set_active(METRIC)
