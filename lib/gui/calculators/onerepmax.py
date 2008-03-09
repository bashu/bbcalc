# -*- coding: utf-8 -*-

""" One-Rep Maximum calculator """

from gettext import gettext as _
from lib.utils import *
from lib.utils.unitconvertor import kg2lb, lb2kg

# General constants
REPCOEF = [0, 1, 0.955, 0.917, 0.885, 0.857, 0.832, 0.809, 
           0.788, 0.769, 0.752, 0.736, 0.721, 0.706, 0.692, 0.678]


class OneRepMax:

    def __init__(self, parent):
        self.parent = parent

        # Get a 'table' with calculator from the XML file
        self.calc_table = self.parent.xml.get_widget('one_rep_max_table')
        self.old_parent = self.calc_table.get_parent()

        # Get several widgets, that will be used later
        self.unit_combobox = self.parent.xml.get_widget('unit_combobox_onerep')
        self.weight_spinbutton = self.parent.xml.get_widget('weight_spinbutton_onerep')
        self.reps_spinbutton = self.parent.xml.get_widget('reps_spinbutton_onerep')
        
        self.onerep_max_entry = self.parent.xml.get_widget('result_entry_onerep')

        # Set active item for unit selection box
        self.unit = 1
        self.unit_combobox.set_active(self.unit)

        # Connect event handlers
        signals = {'on_unit_combobox_onerep_changed' : self.on_unit_combobox_onerep_changed,
                   'on_onerep_max_calc' : self.on_onerep_max_calc}
        self.parent.xml.signal_autoconnect(signals)

    def on_onerep_max_calc(self, *args):
        """
        This formula comes from 'A Practical Approach to Strength Training' by
        Matt Brzycki
        """
        weight = self.weight_spinbutton.get_value()
        max_single = weight / REPCOEF[int(self.reps_spinbutton.get_value())]
        self.onerep_max_entry.set_text(str(round(max_single, 2)))

    def on_unit_combobox_onerep_changed(self, *args):
        """Handle unit conversion"""
        result_unit_label = self.parent.xml.get_widget('result_label_onerep')

        if self.unit != self.unit_combobox.get_active():
            self.unit = self.unit_combobox.get_active()
            weight = self.weight_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit == KILOGRAMMS:
                self.weight_spinbutton.set_value(lb2kg(weight, 2))
            else:
                self.weight_spinbutton.set_value(kg2lb(weight, 2))
            # Change lable for the resulting unit type
            if self.unit_combobox.get_active() != KILOGRAMMS:
                result_unit_label.set_text(_('lbs'))
            else:
                result_unit_label.set_text(_('kg'))
