# -*- coding: utf-8 -*-

"""
Preferences Dialog Box

$Id
"""

import os.path

from lib import GLADE_DIR, HELP_CONTENTS

GLADE_FILE = os.path.join(GLADE_DIR, 'prefs.glade')

import gtk, gnome, gconf

from lib import GCONF_CLIENT, GCONF_MEASUREMENT_SYSTEM, GCONF_DEFAULT_GENDER
from lib import GCONF_GENDER_MALE, GCONF_GENDER_FEMALE
from lib import GCONF_SYSTEM_METRIC, GCONF_SYSTEM_IMPERIAL

from lib.gui.glade import Component
from lib.utils.gconfclass import GConf


class PreferencesDialog(Component, GConf):
    """Shows preferences modal dialog"""
    
    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'prefs_dialog')

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_METRIC:
            self.unit1_radiobutton.set_active(True)
        else:
            self.unit2_radiobutton.set_active(True)
            
        if GCONF_CLIENT.get_string(GCONF_DEFAULT_GENDER) == GCONF_GENDER_MALE:
            self.gender1_radiobutton.set_active(True)
        else:
            self.gender2_radiobutton.set_active(True)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.unit1_notify = self.notify_add(GCONF_MEASUREMENT_SYSTEM, 
                                            self.on_unit1_radiobutton_changed)
        self.unit2_notify = self.notify_add(GCONF_MEASUREMENT_SYSTEM, 
                                            self.on_unit2_radiobutton_changed)

        self.gender1_notify = self.notify_add(GCONF_DEFAULT_GENDER, 
                                              self.on_gender1_radiobutton_changed)
        self.gender2_notify = self.notify_add(GCONF_DEFAULT_GENDER, 
                                              self.on_gender2_radiobutton_changed)

    def show(self):
        self.widget.run()

    def on_helpbutton_clicked(self, *args):
        """Shows help browser"""
        gnome.help_display(HELP_CONTENTS, 'preferences')

    def on_unit1_radiobutton_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_METRIC:
            self.unit1_radiobutton.set_active(True)

    def on_unit2_radiobutton_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
            self.unit2_radiobutton.set_active(True)

    def on_gender1_radiobutton_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_DEFAULT_GENDER) == GCONF_GENDER_MALE:
            self.gender1_radiobutton.set_active(True)

    def on_gender2_radiobutton_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if GCONF_CLIENT.get_string(GCONF_DEFAULT_GENDER) == GCONF_GENDER_FEMALE:
            self.gender2_radiobutton.set_active(True)
      
    def on_unit1_radiobutton_toggled(self, toggle):
        GCONF_CLIENT.set_string(GCONF_MEASUREMENT_SYSTEM, GCONF_SYSTEM_METRIC)
        
    def on_unit2_radiobutton_toggled(self, toggle):
        GCONF_CLIENT.set_string(GCONF_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL)

    def on_gender1_radiobutton_toggled(self, toggle):
        GCONF_CLIENT.set_string(GCONF_DEFAULT_GENDER, GCONF_GENDER_MALE)
        
    def on_gender2_radiobutton_toggled(self, toggle):
        GCONF_CLIENT.set_string(GCONF_DEFAULT_GENDER, GCONF_GENDER_FEMALE)

    def on_prefs_dialog_response(self, dialog, response):
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CLOSE:
            # TODO: Code refactoring
            GCONF_CLIENT.notify_remove(self.unit1_notify)
            GCONF_CLIENT.notify_remove(self.unit2_notify)
            GCONF_CLIENT.notify_remove(self.gender1_notify)
            GCONF_CLIENT.notify_remove(self.gender2_notify)
            dialog.destroy()
