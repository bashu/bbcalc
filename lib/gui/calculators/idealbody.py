# -*- coding: utf-8 -*-

"""
Ideal Body Measurements calculator

$Id$
"""

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'ideal_body.glade')

import gconf
from gettext import gettext as _

from lib.gui.glade import Component

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, DEFAULT_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL
from lib.utils import METRIC, IMPERIAL
from lib.utils.unitconvertor import in2cm, cm2in

# General constants
WRISTCOEF = [6.5, 0.85, 0.70, 0.53, 0.37, 0.36, 0.34, 0.29]


class IdealBody(Component):
    
    description = _("Ideal Body Measurements Calculator")
    unit = None

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'ideal_body_table')

        # List of results
        self.results = [self.wrist_spinbutton, self.chest_entry, self.hip_entry,
                        self.waist_entry, self.thigh_entry, self.neck_entry,
                        self.bicep_entry, self.calve_entry, self.forearm_entry]
        
        # Set active item for unit selection box
        if DEFAULT_MEASUREMENT_SYSTEM == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)   

        self.unit_notify = GCONF_CLIENT.notify_add(GCONF_MEASUREMENT_SYSTEM, \
            lambda x, y, z, a: self.on_unit_combobox_changed(z.value))

    def on_ideal_body_calc(self, *args):
        # Unit conversion
        if self.unit != self.unit_combobox.get_active():
            self.unit = self.unit_combobox.get_active()
            wrist = self.wrist_spinbutton.get_value()
            # Perform conversion for the wrist value
            if self.unit == METRIC:
                self.wrist_spinbutton.set_value(in2cm(wrist, 2))
            else:
                self.wrist_spinbutton.set_value(cm2in(wrist, 2))
        # Results calculation
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

    def on_unit_combobox_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit_combobox.set_active(IMPERIAL)
        else:
            self.unit_combobox.set_active(METRIC)
