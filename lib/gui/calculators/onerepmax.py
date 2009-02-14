# -*- coding: utf-8 -*-

"""
One-Rep Maximum calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'one_rep_max.glade')

import gconf

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator
from lib.utils.gconfclass import GConf

from lib.calculators.onerepmax import onerep_max_calc

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, DEFAULT_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL
from lib.utils import METRIC, IMPERIAL

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (220.0, 100.0)


class OneRepMax(Component, Calculator, GConf):

    unit = None

    def __init__(self, weight=1):
        Component.__init__(self, GLADE_FILE, 'one_rep_max_table')

        self.mass_widgets = {self.unit_combobox.name : [self.weight_spinbutton]}
        self.mass_labels = {self.unit_combobox.name : [self.result_label]}
        self.mass_units = {self.unit_combobox.name : self.unit}

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

        # Default values
        self.default_weight = weight

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'default_weight' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'default_weight':
            self.weight_spinbutton.set_value(value)
        else:
            self.__dict__[name] = value

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        # Set active item for unit selection box
        self.unit_combobox.set_active(DEFAULT_MEASUREMENT_SYSTEM)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.unit_notify = self.notify_add(GCONF_MEASUREMENT_SYSTEM, 
                                           self.on_unit_combobox_changed)

    def on_onerep_max_calc(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_mass(self.unit_combobox.name, 
                                  self.unit_combobox.get_active())

        # Result calculation
        weight = self.weight_spinbutton.get_value()
        reps = self.reps_spinbutton.get_value()

        self.result_entry.set_text(str(onerep_max_calc(weight, int(reps))))

    def on_unit_combobox_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)
