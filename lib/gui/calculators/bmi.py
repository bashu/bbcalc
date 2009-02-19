# -*- coding: utf-8 -*-

"""
Body Mass Index calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'bmi.glade')

import gconf

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator

import lib.utils.config as config

from lib.calculators.bmi import bmi_calc

from lib.utils import METRIC, IMPERIAL

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_HEIGHT = (73.0, 185.0)
DEFAULT_WEIGHT = (165.0, 75.0)


class BMI(Component, Calculator):

    unit1 = unit2 = None

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'bmi_table')

        self.length_widgets = {self.unit1_combobox.name : [self.height_spinbutton]}
        self.length_units = {self.unit1_combobox.name : self.unit1}

        self.mass_widgets = {self.unit2_combobox.name : [self.weight_spinbutton]}
        self.mass_units = {self.unit2_combobox.name : self.unit2}

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'height', 'weight' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'height':
            self.height_spinbutton.set_value(value)
        if name == 'weight':
            self.weight_spinbutton.set_value(value)
        else:
            self.__dict__[name] = value

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()
        # Set active item for unit selection box
        self.unit1_combobox.set_active(self.config.measurement_system)
        self.unit2_combobox.set_active(self.config.measurement_system)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)

    def on_bmi_calc(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_length(self.unit1_combobox.name, 
                                    self.unit1_combobox.get_active())

        self.unit_conversion_mass(self.unit2_combobox.name, 
                                  self.unit2_combobox.get_active())

        # Result calculation
        height = self.height_spinbutton.get_value()
        weight = self.weight_spinbutton.get_value()

        height_unit = self.unit1_combobox.get_active()
        weight_unit = self.unit2_combobox.get_active()

        result = bmi_calc(height, weight, height_unit, weight_unit)

        self.result1_entry.set_text(str(result['bmi']))
        
        self.result2_label.set_text(str(result['status']))

    def on_gconf_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(IMPERIAL)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(METRIC)
