# -*- coding: utf-8 -*-

"""
Ideal Body Measurements calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'ideal_body.glade')

import gconf

from lib.gui.glade import Component
from lib.gui.calculators.calculator import Calculator
from lib.utils.gconfclass import GConf

from lib.calculators.idealbody import ideal_body_calc

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, DEFAULT_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL
from lib.utils import METRIC, IMPERIAL

# Predefined values, used somewhere else
DEFAULT_WRIST = (6.89, 17.5)


class IdealBody(Component, Calculator, GConf):

    unit = None

    def __init__(self, wrist=1):
        Component.__init__(self, GLADE_FILE, 'ideal_body_table')
        
        # List of results
        self.results = [self.wrist_spinbutton, self.chest_entry, self.hip_entry,
                        self.waist_entry, self.thigh_entry, self.neck_entry,
                        self.bicep_entry, self.calve_entry, self.forearm_entry]

        self.length_widgets = {self.unit_combobox.name :
                               [self.wrist_spinbutton]}
        self.length_units = {self.unit_combobox.name : self.unit}
        
        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()
        
        # Default values
        self.default_wrist = wrist

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'default_wrist' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'default_wrist':
            self.wrist_spinbutton.set_value(value)
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

    def on_ideal_body_calc(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_length(self.unit_combobox.name, 
                                    self.unit_combobox.get_active())

        results_array = ideal_body_calc(self.wrist_spinbutton.get_value())

        for idx in xrange(1, len(self.results)):
            self.results[idx].set_text(str(results_array[idx]))

    def on_unit_combobox_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)
