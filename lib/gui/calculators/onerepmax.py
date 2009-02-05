# -*- coding: utf-8 -*-

"""
One-Rep Maximum calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'one_rep_max.glade')

import gconf
from gettext import gettext as _

from lib.gui.glade import Component

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, DEFAULT_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL
from lib.utils import METRIC, IMPERIAL
from lib.utils.unitconvertor import kg2lb, lb2kg

# General constants
REPCOEF = [0, 1, 0.955, 0.917, 0.885, 0.857, 0.832, 0.809, 
           0.788, 0.769, 0.752, 0.736, 0.721, 0.706, 0.692, 0.678]


class OneRepMax(Component):
    
    description = _("One-Rep Max Calculator")
    unit = None
    
    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'one_rep_max_table')

        # Set active item for unit selection box
        if DEFAULT_MEASUREMENT_SYSTEM == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)
        
        self.unit_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit_combobox_changed(z.value))

    def on_onerep_max_calc(self, *args):
        """
        This formula comes from 'A Practical Approach to Strength Training' by
        Matt Brzycki
        """
        # Unit conversion
        if self.unit != self.unit_combobox.get_active():
            self.unit = self.unit_combobox.get_active()
            weight = self.weight_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit == METRIC:
                self.weight_spinbutton.set_value(lb2kg(weight, 2))
            else:
                self.weight_spinbutton.set_value(kg2lb(weight, 2))
            # Change label for the resulting unit type
            if self.unit_combobox.get_active() != METRIC:
                self.result_label.set_text(_('lbs'))
            else:
                self.result_label.set_text(_('kg'))
        # Result calculation
        weight = self.weight_spinbutton.get_value()
        max_single = weight / REPCOEF[int(self.reps_spinbutton.get_value())]
        self.result_entry.set_text(str(round(max_single, 2)))

    def on_unit_combobox_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)
