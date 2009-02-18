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

import lib.utils.config as config

from lib.calculators.idealbody import ideal_body_calc

from lib.utils import METRIC, IMPERIAL

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WRIST = (6.89, 17.5)


class IdealBody(Component, Calculator):

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
        self.wrist = wrist

    def __delattr__(self, name):
        """Delete attributes method."""
        nodelete = ( 'wrist' )

        if name in nodelete:
            raise TypeError, name + " property cannot be deleted"
        else:
            del self.__dict__[name]

    def __setattr__(self, name, value):
        """Set attributes method."""
        if name == 'wrist':
            self.wrist_spinbutton.set_value(value)
        else:
            self.__dict__[name] = value

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()
        # Set active item for unit selection box
        self.unit_combobox.set_active(self.config.measurement_system)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)

    def on_ideal_body_calc(self, *args):
        # Perform unit conversion if needed
        self.unit_conversion_length(self.unit_combobox.name, 
                                    self.unit_combobox.get_active())

        results_array = ideal_body_calc(self.wrist_spinbutton.get_value())

        for idx in xrange(1, len(self.results)):
            self.results[idx].set_text(str(results_array[idx]))

    def on_gconf_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit_combobox.set_active(METRIC)
