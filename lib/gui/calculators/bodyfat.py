# -*- coding: utf-8 -*-

"""
Body Fat calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'bodyfat.glade')

import gconf

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator

import lib.utils.config as config

from lib.calculators.bodyfat import bodyfat_calc

from lib.utils import METRIC, IMPERIAL, MALE, FEMALE

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WAIST = (32.0, 81.5)
DEFAULT_WEIGHT = (220.0, 100.0)


class Bodyfat(Component, Calculator):

    unit1 = unit2 = None
    gender = None

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'bodyfat_table')

        self.length_widgets = {self.unit1_combobox.name :
                               [self.waist_spinbutton]}
        self.length_units = {self.unit1_combobox.name : self.unit1}
        
        self.mass_widgets = {self.unit2_combobox.name : 
                             [self.weight_spinbutton]}
        self.mass_labels = {self.unit2_combobox.name :
                           [self.result1_label, self.result2_label]}
        self.mass_units = {self.unit2_combobox.name : self.unit2}

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'waist', 'weight', 'gender' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'waist':
            self.waist_spinbutton.set_value(value)
        if name == 'weight':
            self.weight_spinbutton.set_value(value)
        if name == 'gender':
            self.gender_combobox.set_active(value)
        else:
            self.__dict__[name] = value

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()
        # Set active item for unit selection box
        self.unit1_combobox.set_active(self.config.measurement_system)
        self.unit2_combobox.set_active(self.config.measurement_system)
        self.gender_combobox.set_active(self.config.default_gender)  

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)
        self.config.notify_add(config.GCONF_DEFAULT_GENDER, self.on_gconf_changed)

    def on_bodyfat_calc(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_length(self.unit1_combobox.name, 
                                    self.unit1_combobox.get_active())

        self.unit_conversion_mass(self.unit2_combobox.name, 
                                  self.unit2_combobox.get_active())

        # Results calculation
        waist = self.waist_spinbutton.get_value()        
        weight = self.weight_spinbutton.get_value()
        waist_unit = self.unit1_combobox.get_active()
        weight_unit = self.unit2_combobox.get_active()
        gender = self.gender_combobox.get_active()

        result = bodyfat_calc(waist, weight, waist_unit, weight_unit, gender)   

        # Set results        
        self.percent_entry.set_text(str(result['bodyfat']))
        self.fat_entry.set_text(str(result['fatweight']))
        self.lean_entry.set_text(str(result['lbm']))
        self.calories_entry.set_text(str(result['calories']))

        # Set classification
        self.result3_label.set_text(result['classification'])

    def on_gconf_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(IMPERIAL)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(METRIC)
        if value.get_string() == config.GCONF_GENDER_MALE:
            self.gender_combobox.set_active(MALE)
        if value.get_string() == config.GCONF_GENDER_FEMALE:
            self.gender_combobox.set_active(FEMALE)
