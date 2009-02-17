# -*- coding: utf-8 -*-

"""
Main Application class

$Id
"""

# GTK/Gnome stuff
try:
    import pygtk
    pygtk.require('2.0')
except:
    pass
try:
    import gtk
    import gtk.glade
    import gnome
except:
    import sys
    sys.exit(1)

import os.path
from lib import GLADE_DIR, HELP_CONTENTS

GLADE_FILE = os.path.join(GLADE_DIR, 'bbcalc.glade')

from lib.gui.glade import Component

from lib import DEFAULT_MEASUREMENT_SYSTEM, DEFAULT_GENDER

import lib.gui.calculators.idealbody as idealbody
import lib.gui.calculators.onerepmax as onerepmax
import lib.gui.calculators.bodyfat as bodyfat
import lib.gui.calculators.bmi as bmi


class MainApp(Component):
    """Create application based on a MainFrame class"""
    
    # Defaults
    _menu_cix = -1

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'main_window')

        # Create calculators tables
        self.create_tables()

        # Show main window and goes to main loop (it's hidden by default)
        self.main_window.show()
        
    def app_quit(self, *args):
        """Quits application"""
        gtk.main_quit()

    def set_panel(self, panel):
        """Set working panel"""
        if hasattr(self, 'panel'):
            self.calc_box.remove(self.panel.widget)
        self.panel = panel
        self.calc_box.add(panel.widget)

    def create_tables(self):
        """Create calculators tables and set default panel"""
        # Create dictionary of calculators
        # TODO: Clean this shit
        self.calculators = {'onerep_max' : onerepmax.OneRepMax(weight=onerepmax.DEFAULT_WEIGHT[DEFAULT_MEASUREMENT_SYSTEM]),
                            'ideal_body' : idealbody.IdealBody(wrist=idealbody.DEFAULT_WRIST[DEFAULT_MEASUREMENT_SYSTEM]),
                            'bodyfat' : bodyfat.Bodyfat(waist=bodyfat.DEFAULT_WAIST[DEFAULT_MEASUREMENT_SYSTEM],
                                                        weight=bodyfat.DEFAULT_WEIGHT[DEFAULT_MEASUREMENT_SYSTEM],
                                                        gender=DEFAULT_GENDER),
                            'body_mass_index' : bmi.BMI(height=bmi.DEFAULT_HEIGHT[DEFAULT_MEASUREMENT_SYSTEM], weight=bmi.DEFAULT_WEIGHT[DEFAULT_MEASUREMENT_SYSTEM])}
        # Set default panel
        self.set_panel(self.calculators['bodyfat'])

    def on_menuitem_select(self, item, *args):
        """Set statusbar text for selected menu item"""
        if item.get_tooltip_text() is not None:
            self.statusbar.push(self._menu_cix, item.get_tooltip_text())

    def on_menuitem_deselect(self, item, *args):
        if item.get_tooltip_text() is not None:
            self.statusbar.pop(self._menu_cix)
        
    def on_main_window_destroy(self, *args):
        self.app_quit(args)

    def on_quit_activate(self, *args):
        self.app_quit(args)

    def on_preferences_activate(self, *args):
        """Shows Preferences dialog box"""
        from lib.gui.preferences import PreferencesDialog
        prefs_dialog = PreferencesDialog()
        prefs_dialog.show()

    def on_help_activate(self, *args):
        """Shows help browser"""
        gnome.help_display(HELP_CONTENTS)

    def on_about_activate(self, *args):
        """Shows About dialog box"""
        from lib.gui.about import AboutDialog
        about_dialog = AboutDialog()
        about_dialog.show()

    def on_calculator_activate(self, widget):
        """Activate selected calculator"""
        if widget.get_active() == True:
            # widget.name is short name of selected calculator
            self.set_panel(self.calculators[widget.name])

def main(name, version):
    gnome.init(name, version)

    app = MainApp()
    gtk.main()
