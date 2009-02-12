# -*- coding: utf-8 -*-

"""
Body Fat calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'bodyfat.glade')

import gconf
from gettext import gettext as _

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator

from lib.calculators.bodyfat import bodyfat_calc

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, GCONF_DEFAULT_GENDER
from lib import DEFAULT_MEASUREMENT_SYSTEM, DEFAULT_GENDER
from lib import GCONF_SYSTEM_IMPERIAL, GCONF_GENDER_MALE
from lib.utils import METRIC, IMPERIAL
from lib.utils import MALE, FEMALE


class Bodyfat(Component, Calculator):

    description = _(u'Body Fat Estimator')
    default_waist = [31.5, 80.0]
    default_weight = [176.0, 80.0]
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

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        # Set active item for unit selection box
        if DEFAULT_MEASUREMENT_SYSTEM == GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(IMPERIAL)
        else:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(METRIC)  
        # Set default values
        self.waist_spinbutton.set_value(self.default_waist[self.unit1_combobox.get_active()])
        self.weight_spinbutton.set_value(self.default_weight[self.unit2_combobox.get_active()])

        if DEFAULT_GENDER == GCONF_GENDER_MALE:
            self.gender_combobox.set_active(MALE)
        else:
            self.gender_combobox.set_active(FEMALE)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.unit1_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit1_combobox_changed(z.value))
        self.unit2_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit2_combobox_changed(z.value))
        self.gender_notify = GCONF_CLIENT.notify_add(GCONF_DEFAULT_GENDER, \
            lambda x, y, z, a: self.on_gender_combobox_changed(z.value))

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

    def on_unit1_combobox_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
        else:
            self.unit1_combobox.set_active(METRIC)

    def on_unit2_combobox_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit2_combobox.set_active(IMPERIAL)
        else:
            self.unit2_combobox.set_active(METRIC)

    def on_gender_combobox_changed(self, value):
        """Handle gender changing"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_DEFAULT_GENDER) == GCONF_GENDER_MALE:
            self.gender_combobox.set_active(MALE)
        else:
            self.gender_combobox.set_active(FEMALE)
