# -*- coding: utf-8 -*-

"""
Weight Units Converter

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'weightunits.glade')

import gconf

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator

import lib.utils.config as config

from lib.utils.unitconvertor import lb2kg, kg2lb

from lib.utils import METRIC, IMPERIAL

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (165.0, 75.0)
#WEIGHT_UNITS = (u'Ounces', u'Pounds', u'Milligrams', u'Grams' u'Kilograms')

class WeightUnitsConverter(Component, Calculator):

    unit1 = unit2 = None

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'weightunits_table')

        self.mass_widgets = {self.unit1_combobox.name : [self.weight_spinbutton]}
        self.mass_units = {self.unit1_combobox.name : self.unit1}

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'weight' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'weight':
            self.weight_spinbutton.set_value(value)
        else:
            self.__dict__[name] = value

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()
        # Set active item for unit selection box
        if self.config.measurement_system == IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(METRIC)
        else:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(IMPERIAL)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)

    def on_calculation(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_mass(self.unit1_combobox.name, 
                                  self.unit1_combobox.get_active())

        # Result calculation
        weight = self.weight_spinbutton.get_value()

        if self.unit1_combobox.get_active() == IMPERIAL:
            if self.unit2_combobox.get_active() == METRIC:
                result = lb2kg(weight)
            else:
                result = weight
        elif self.unit1_combobox.get_active() == METRIC:
            if self.unit2_combobox.get_active() == IMPERIAL:
                result = kg2lb(weight)
            else:
                result =  weight

        self.result_entry.set_text(str(result))

    def on_gconf_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(METRIC)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(IMPERIAL)
