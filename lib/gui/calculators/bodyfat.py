# -*- coding: utf-8 -*-

"""
Bodyfat calculator

$Id$
"""

from gettext import gettext as _
from lib.utils import KILOGRAMMS, POUNDS, CENTIMETERS, FEMALE
from lib.utils.unitconvertor import kg2lb, lb2kg, in2cm, cm2in

# General constants
MALECOEF = 98.42
FEMALECOEF = 76.76

WAISTCOEF = 4.15
WEIGHTCOEF = 1.082

CALORIESCOEF = 13.83


class Bodyfat:

    def __init__(self, parent):
        self.parent = parent

        # Get a 'table' with calculator from the XML file
        self.calc_table = self.parent.xml.get_widget('bodyfat_table')
        self.old_parent = self.calc_table.get_parent()

        # Get several widgets, that will be used later
        self.unit1_combobox = self.parent.xml.get_widget('unit1_combobox_bodyfat')
        self.unit2_combobox = self.parent.xml.get_widget('unit2_combobox_bodyfat')
        self.gender_combobox = self.parent.xml.get_widget('gender_combobox_bodyfat')
        self.waist_spinbutton = self.parent.xml.get_widget('waist_spinbutton_bodyfat')
        self.weight_spinbutton = self.parent.xml.get_widget('weight_spinbutton_bodyfat')

        self.percent_entry = self.parent.xml.get_widget('percent_entry_bodyfat')
        self.fat_entry = self.parent.xml.get_widget('fat_entry_bodyfat')
        self.lean_entry = self.parent.xml.get_widget('lean_entry_bodyfat')
        self.calories_entry = self.parent.xml.get_widget('calories_entry_bodyfat')

        # Set active item for unit selection box
        self.unit1 = self.unit2 = 1 # 1 - Centimeters / Kilogramms, 0 - Inches / Pounds
        self.unit1_combobox.set_active(self.unit1)
        self.unit2_combobox.set_active(self.unit2)
        self.gender = 0 # 0 - Male, 1 - Female
        self.gender_combobox.set_active(self.gender)

        # Connect event handlers
        signals = {'on_unit1_combobox_bodyfat_changed' : self.on_unit1_combobox_bodyfat_changed,
                   'on_unit2_combobox_bodyfat_changed' : self.on_unit2_combobox_bodyfat_changed,
                   'on_gender_combobox_changed' : self.on_gender_combobox_bodyfat_changed,
                   'on_bodyfat_calc' : self.on_bodyfat_calc}
        self.parent.xml.signal_autoconnect(signals)

    def on_bodyfat_calc(self, *args):
        """This formula comes from 'The Bodyfat Guide' by Ron Brown"""
        waist = self.waist_spinbutton.get_value()        
        weight = self.weight_spinbutton.get_value()

        if self.unit1_combobox.get_active() == CENTIMETERS:
            waist = cm2in(float(waist))
        if self.unit2_combobox.get_active() == KILOGRAMMS:
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
        if self.unit2_combobox.get_active() == KILOGRAMMS:
            factor = POUNDS
        else:
            factor = KILOGRAMMS
        
        # Set results        
        self.percent_entry.set_text(str(round(bodyfat, 2)))
        self.fat_entry.set_text(str(round(fatweight / factor, 2)))
        self.lean_entry.set_text(str(round(lbm / factor, 2)))
        self.calories_entry.set_text(str(round(lbm * CALORIESCOEF, 0)))
        
        # Set classification
        result3_unit_label = self.parent.xml.get_widget('result3_label_bodyfat')
        if self.gender_combobox.get_active() == FEMALE:
            if bodyfat < 5.0:
                result3_unit_label.set_text(_('Essential Fat'))
            if bodyfat > 5.0 and bodyfat < 14.0:
                result3_unit_label.set_text(_('Athletes'))
            if bodyfat > 14.0 and bodyfat < 18.0:
                result3_unit_label.set_text(_('Fitness'))
            if bodyfat > 18.0 and bodyfat < 25.0:
                result3_unit_label.set_text(_('Acceptable'))
            if bodyfat > 25.0:
                result3_unit_label.set_text(_('Obese'))
        else:
            if bodyfat < 14.0:
                result3_unit_label.set_text(_('Essential Fat'))
            if bodyfat > 14.0 and bodyfat < 21.0:
                result3_unit_label.set_text(_('Athletes'))
            if bodyfat > 21.0 and bodyfat < 25.0:
                result3_unit_label.set_text(_('Fitness'))
            if bodyfat > 25.0 and bodyfat < 32.0:
                result3_unit_label.set_text(_('Acceptable'))
            if bodyfat > 32.0:
                result3_unit_label.set_text(_('Obese'))
                

    def on_unit1_combobox_bodyfat_changed(self, *args):
        """Handle unit conversion"""
        if self.unit1 != self.unit1_combobox.get_active():
            self.unit1 = self.unit1_combobox.get_active()
            waist = self.waist_spinbutton.get_value()
            if self.unit1 == CENTIMETERS:
                self.waist_spinbutton.set_value(in2cm(waist, 2))
            else:
                self.waist_spinbutton.set_value(cm2in(waist, 2))

    def on_unit2_combobox_bodyfat_changed(self, *args):
        """Handle unit conversion"""
        result1_unit_label = self.parent.xml.get_widget('result1_label_bodyfat')
        result2_unit_label = self.parent.xml.get_widget('result2_label_bodyfat')

        if self.unit2 != self.unit2_combobox.get_active():
            self.unit2 = self.unit2_combobox.get_active()
            weight = self.weight_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit2 == KILOGRAMMS:
                self.weight_spinbutton.set_value(lb2kg(weight, 2))
            else:
                self.weight_spinbutton.set_value(kg2lb(weight, 2))
            # Change label for the resulting unit type
            if self.unit2_combobox.get_active() != KILOGRAMMS:
                result1_unit_label.set_text(_('lbs'))
                result2_unit_label.set_text(_('lbs'))
            else:
                result1_unit_label.set_text(_('kg'))
                result2_unit_label.set_text(_('kg'))

    def on_gender_combobox_bodyfat_changed(self, *args):
        """Handle unit conversion"""
        pass
