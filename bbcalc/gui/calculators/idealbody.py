## -*- coding: utf-8 -*-


import gconf

from kiwi.ui.delegates import SlaveDelegate

import bbcalc.utils.config as config

from bbcalc.calculators.idealbody import ideal_body_calc

from bbcalc.utils import METRIC, IMPERIAL
from bbcalc.utils.unitconvertor import convert_length

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WRIST = (6.89, 17.5)


class IdealBody(SlaveDelegate):
    gladefile = 'ideal_body_window'

    def __init__(self):
        SlaveDelegate.__init__(self)

        # List of result widgets
        self.results = [self.wrist_spinbutton, self.chest_entry, self.hip_entry,
                        self.waist_entry, self.thigh_entry, self.neck_entry,
                        self.bicep_entry, self.calve_entry, self.forearm_entry]

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
        self.wrist_spinbutton.set_value(DEFAULT_WRIST[self.config.measurement_system])

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)

    # Signal handlers

    def after_unit_combobox__changed(self, entry, *args):
        active = entry.get_active()
        wrist = self.wrist_spinbutton.get_value()
        self.wrist_spinbutton.set_value(convert_length(wrist, active))

    def after_wrist_spinbutton__changed(self, entry, *args):
        # Result calculation
        wrist = entry.get_value() or None
        results = ideal_body_calc(wrist)

        # Exclude first widget in self.results
        for idx in xrange(1, len(self.results)):
            self.results[idx].set_text(str(results[idx]))

    def on_gconf_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit_combobox.set_active(METRIC)
