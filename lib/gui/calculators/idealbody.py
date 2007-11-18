# -*- coding: utf-8 -*-

""" Ideal Body Measurements calculator """

from gettext import gettext as _
from lib.utils import *
from lib.utils.unitconvertor import in2cm, cm2in

WRISTCOEF = [6.5, 0.85, 0.70, 0.53, 0.37, 0.36, 0.34, 0.29]


class IdealBody:

    def __init__(self, parent):
        self.parent = parent

        # Get a 'table' with calculator from the XML file
        self.calc_table = self.parent.xml.get_widget('ideal_body_table')
        self.old_parent = self.calc_table.get_parent()

        # Get several widgets, that will be used later
        self.unit_combobox = self.parent.xml.get_widget('unit_combobox_ideal')
        self.wrist_spinbutton = self.parent.xml.get_widget('wrist_spinbutton_ideal')

        self.chest_entry = self.parent.xml.get_widget('chest_entry_ideal')
        self.waist_entry = self.parent.xml.get_widget('waist_entry_ideal')
        self.hip_entry = self.parent.xml.get_widget('hip_entry_ideal')
        self.bicep_entry = self.parent.xml.get_widget('bicep_entry_ideal')
        self.forearm_entry = self.parent.xml.get_widget('forearm_entry_ideal')
        self.thigh_entry = self.parent.xml.get_widget('thigh_entry_ideal')
        self.calve_entry = self.parent.xml.get_widget('calve_entry_ideal')
        self.neck_entry = self.parent.xml.get_widget('neck_entry_ideal')

        self.results = [self.wrist_spinbutton, self.chest_entry, self.hip_entry,
                        self.waist_entry, self.thigh_entry, self.neck_entry,
                        self.bicep_entry, self.calve_entry, self.forearm_entry]
        
        # Set active item for unit selection box
        self.unit = 1
        self.unit_combobox.set_active(self.unit)
        
        # Connect event handlers
        signals = {'on_unit_combobox_ideal_changed' : self.on_unit_combobox_ideal_changed,
                   'on_ideal_body_calc' : self.on_ideal_body_calc}
        self.parent.xml.signal_autoconnect(signals)

    def on_ideal_body_calc(self, *args):
        wrist = self.wrist_spinbutton.get_value()    
        array = [wrist]
        array.append(array[0] * WRISTCOEF[0])
        for idx in xrange(1, 8):
            array.append(array[1] * WRISTCOEF[idx])

        for idx in xrange(0, 9):
            array[idx] = round((array[idx] + 0.0001) * 100, 2)
            array[idx] = round(array[idx] / 100.0, 2)

        for idx in xrange(1, 9):
            self.results[idx].set_text(str(array[idx]))

    def on_unit_combobox_ideal_changed(self, *args):
        """Handle unit conversion"""
        if self.unit != self.unit_combobox.get_active():
            self.unit = self.unit_combobox.get_active()
            wrist = self.wrist_spinbutton.get_value()
            # Perform conversion for the weight value
            if self.unit == CENTIMETERS:
                self.wrist_spinbutton.set_value(in2cm(wrist, 2))
            else:
                self.wrist_spinbutton.set_value(cm2in(wrist, 2))


