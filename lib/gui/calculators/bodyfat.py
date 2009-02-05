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

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, GCONF_DEFAULT_GENDER
from lib import DEFAULT_MEASUREMENT_SYSTEM, DEFAULT_GENDER
from lib import GCONF_SYSTEM_IMPERIAL, GCONF_GENDER_MALE
from lib.utils import METRIC, IMPERIAL
from lib.utils import KILOGRAMMS, POUNDS, MALE, FEMALE
from lib.utils.unitconvertor import kg2lb, lb2kg, in2cm, cm2in

# General constants
MALECOEF = 98.42
FEMALECOEF = 76.76

WAISTCOEF = 4.15
WEIGHTCOEF = 1.082

CALORIESCOEF = 13.83


class Bodyfat(Component):

    description = _("Body Fat Estimator")
    unit1 = unit2 = None
    gender = None

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'bodyfat_table')

        # Set active item for unit selection box
        if DEFAULT_MEASUREMENT_SYSTEM == GCONF_SYSTEM_IMPERIAL:
            self.unit1_combobox.set_active(IMPERIAL)
            self.unit2_combobox.set_active(IMPERIAL)
        else:
            self.unit1_combobox.set_active(METRIC)
            self.unit2_combobox.set_active(METRIC)   

        if DEFAULT_GENDER == GCONF_GENDER_MALE:
            self.gender_combobox.set_active(MALE)
        else:
            self.gender_combobox.set_active(FEMALE)

        self.unit1_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit1_combobox_changed(z.value))
        self.unit2_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit2_combobox_changed(z.value))
        self.gender_notify = GCONF_CLIENT.notify_add(GCONF_DEFAULT_GENDER, \
            lambda x, y, z, a: self.on_gender_combobox_changed(z.value))

    def on_bodyfat_calc(self, *args):
        """This formula comes from 'The Bodyfat Guide' by Ron Brown"""
        # Unit conversion for waist size
        if self.unit1 != self.unit1_combobox.get_active():
            self.unit1 = self.unit1_combobox.get_active()
            waist = self.waist_spinbutton.get_value()
            if self.unit1 == METRIC:
                self.waist_spinbutton.set_value(in2cm(waist, 2))
            else:
                self.waist_spinbutton.set_value(cm2in(waist, 2))
        # Unit conversion for weight
        if self.unit2 != self.unit2_combobox.get_active():
            self.unit2 = self.unit2_combobox.get_active()
            weight = self.weight_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit2 == METRIC:
                self.weight_spinbutton.set_value(lb2kg(weight, 2))
            else:
                self.weight_spinbutton.set_value(kg2lb(weight, 2))
            # Change label for the resulting unit type
            if self.unit2_combobox.get_active() != METRIC:
                self.result1_label.set_text(_('lbs'))
                self.result2_label.set_text(_('lbs'))
            else:
                self.result1_label.set_text(_('kg'))
                self.result2_label.set_text(_('kg'))

        # Results calculation
        waist = self.waist_spinbutton.get_value()        
        weight = self.weight_spinbutton.get_value()

        if self.unit1_combobox.get_active() == METRIC:
            waist = cm2in(float(waist))
        if self.unit2_combobox.get_active() == METRIC:
            weight = kg2lb(float(weight))
        tmp_waist = float(waist) * WAISTCOEF
        tmp_weight = float(weight) * WEIGHTCOEF
        diff = tmp_weight - tmp_waist;
        if self.gender_combobox.get_active() == FEMALE:
            lbm = diff + FEMALECOEF;
        else:
            lbm = diff + MALECOEF;
        fatweight = float(weight) - lbm;
        bodyfat = fatweight / float(weight) * 100.0;
        if self.unit2_combobox.get_active() == METRIC:
            factor = POUNDS
        else:
            factor = KILOGRAMMS
        
        # Set results        
        self.percent_entry.set_text(str(round(bodyfat, 2)))
        self.fat_entry.set_text(str(round(fatweight / factor, 2)))
        self.lean_entry.set_text(str(round(lbm / factor, 2)))
        self.calories_entry.set_text(str(round(lbm * CALORIESCOEF, 0)))
        
        # Set classification
        if self.gender_combobox.get_active() == FEMALE:
            if bodyfat < 5.0:
                self.result3_label.set_text(_('Essential Fat'))
            if bodyfat > 5.0 and bodyfat < 14.0:
                self.result3_label.set_text(_('Athletes'))
            if bodyfat > 14.0 and bodyfat < 18.0:
                self.result3_label.set_text(_('Fitness'))
            if bodyfat > 18.0 and bodyfat < 25.0:
                self.result3_label.set_text(_('Acceptable'))
            if bodyfat > 25.0:
                self.result3_label.set_text(_('Obese'))
        else:
            if bodyfat < 14.0:
                self.result3_label.set_text(_('Essential Fat'))
            if bodyfat > 14.0 and bodyfat < 21.0:
                self.result3_label.set_text(_('Athletes'))
            if bodyfat > 21.0 and bodyfat < 25.0:
                self.result3_label.set_text(_('Fitness'))
            if bodyfat > 25.0 and bodyfat < 32.0:
                self.result3_label.set_text(_('Acceptable'))
            if bodyfat > 32.0:
                self.result3_label.set_text(_('Obese'))              

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