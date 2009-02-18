# -*- coding: utf-8 -*-

"""
Preferences Dialog Box

$Id
"""

import os.path

from lib import GLADE_DIR, HELP_CONTENTS

GLADE_FILE = os.path.join(GLADE_DIR, 'prefs.glade')

import gtk, gnome, gconf

from lib.gui.glade import Component

import lib.utils.config as config
from lib.utils import METRIC, IMPERIAL, MALE, FEMALE


class PreferencesDialog(Component):
    """Shows preferences modal dialog"""
    
    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'prefs_dialog')

        # Loading default values from GConf
        self.load_gconf_defaults()
        # Creating GConf notification handlers
        self.create_gconf_notification()

    def load_gconf_defaults(self):
        """Load GConf defaults"""
        self.config = config.Config()

        if self.config.measurement_system == IMPERIAL:
            self.unit1_radiobutton.set_active(True)
        else:
            self.unit2_radiobutton.set_active(True)
            
        if self.config.default_gender == MALE:
            self.gender1_radiobutton.set_active(True)
        else:
            self.gender2_radiobutton.set_active(True)

    def create_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)
        self.config.notify_add(config.GCONF_DEFAULT_GENDER, self.on_gconf_changed)

    def show(self):
        self.widget.run()

    def on_helpbutton_clicked(self, *args):
        """Shows help browser"""
        gnome.help_display(HELP_CONTENTS, 'preferences')

    def on_gconf_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.unit1_radiobutton.set_active(True)
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.unit2_radiobutton.set_active(True)
        if value.get_string() == config.GCONF_GENDER_MALE:
            self.gender1_radiobutton.set_active(True)
        if value.get_string() == config.GCONF_GENDER_FEMALE:
            self.gender2_radiobutton.set_active(True)

    def on_unit1_radiobutton_toggled(self, toggle):
        self.config.measurement_system = IMPERIAL

    def on_unit2_radiobutton_toggled(self, toggle):
        self.config.measurement_system = METRIC

    def on_gender1_radiobutton_toggled(self, toggle):
        self.config.default_gender = MALE

    def on_gender2_radiobutton_toggled(self, toggle):
        self.config.default_gender = FEMALE

    def on_prefs_dialog_response(self, dialog, response):
        if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CLOSE:
            dialog.destroy()
