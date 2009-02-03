# -*- coding: utf-8 -*-

"""
One-Rep Maximum calculator

$Id$
"""

import os.path
from lib.paths import glade_dir

GLADE_FILE = os.path.join(glade_dir, 'one_rep_max.glade')

from gettext import gettext as _

from lib.gui.glade import Component

from lib.utils import KILOGRAMMS
from lib.utils.unitconvertor import kg2lb, lb2kg

# General constants
REPCOEF = [0, 1, 0.955, 0.917, 0.885, 0.857, 0.832, 0.809, 
           0.788, 0.769, 0.752, 0.736, 0.721, 0.706, 0.692, 0.678]


class OneRepMax(Component):
    
    description = _("One-Rep Max Calculator")
    
    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'one_rep_max_table')

        # Set active item for unit selection box
        self.unit = 1   # 1 - Kilogramms, 0 - Pounds
        self.unit_combobox.set_active(self.unit)

    def on_onerep_max_calc(self, *args):
        """
        This formula comes from 'A Practical Approach to Strength Training' by
        Matt Brzycki
        """
        weight = self.weight_spinbutton.get_value()
        max_single = weight / REPCOEF[int(self.reps_spinbutton.get_value())]
        self.result_entry.set_text(str(round(max_single, 2)))

    def on_unit_combobox_onerep_changed(self, *args):
        """Handle unit conversion"""
        if self.unit != self.unit_combobox.get_active():
            self.unit = self.unit_combobox.get_active()
            weight = self.weight_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit == KILOGRAMMS:
                self.weight_spinbutton.set_value(lb2kg(weight, 2))
            else:
                self.weight_spinbutton.set_value(kg2lb(weight, 2))
            # Change label for the resulting unit type
            if self.unit_combobox.get_active() != KILOGRAMMS:
                self.result_label.set_text(_('lbs'))
            else:
                self.result_label.set_text(_('kg'))
