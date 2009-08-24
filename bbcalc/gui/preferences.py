# -*- coding: utf-8 -*-

import gtk, gnome, gconf

import bbcalc.utils.config as config

from kiwi.ui.delegates import Delegate

from bbcalc.utils import METRIC, IMPERIAL, MALE, FEMALE


class PreferencesDialog(Delegate):
    """Shows preferences modal dialog"""

    gladefile = 'preferences_window'

    def __init__(self):
        Delegate.__init__(self, delete_handler=self.quit_if_last)

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

    def on_close_button__clicked(self, *args):
        self.hide_and_quit()

#    def on_helpbutton_clicked(self, *args):
#        """Shows help browser"""
#        gnome.help_display(HELP_CONTENTS, 'preferences')

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

    def after_unit1_radiobutton__toggled(self, *args):
        self.config.measurement_system = IMPERIAL

    def after_unit2_radiobutton__toggled(self, *args):
        self.config.measurement_system = METRIC

    def on_gender1_radiobutton__toggled(self, *args):
        self.config.default_gender = MALE

    def on_gender2_radiobutton__toggled(self, *args):
        self.config.default_gender = FEMALE
