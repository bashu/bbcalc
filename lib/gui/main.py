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

import lib.utils.config as config

import lib.gui.calculators.idealbody as idealbody
import lib.gui.calculators.onerepmax as onerepmax
import lib.gui.calculators.bodyfat as bodyfat
import lib.gui.calculators.bmi as bmi
import lib.gui.calculators.running as running
import lib.gui.calculators.weightunits as weightunits


class MainApp(Component):
    """Create application based on a MainFrame class"""
    
    # Defaults
    _menu_cix = -1

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'main_window')

        self.config = config.Config()

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
        onerep_max_calc = onerepmax.OneRepMax()
        onerep_max_calc.weight = onerepmax.DEFAULT_WEIGHT[self.config.measurement_system]

        idealbody_calc = idealbody.IdealBody()
        idealbody_calc.wrist = idealbody.DEFAULT_WRIST[self.config.measurement_system]

        bodyfat_calc = bodyfat.Bodyfat()
        bodyfat_calc.waist = bodyfat.DEFAULT_WAIST[self.config.measurement_system]
        bodyfat_calc.weight = bodyfat.DEFAULT_WEIGHT[self.config.measurement_system]

        bmi_calc = bmi.BMI() 
        bmi_calc.height = bmi.DEFAULT_HEIGHT[self.config.measurement_system]
        bmi_calc.weight = bmi.DEFAULT_WEIGHT[self.config.measurement_system]
        
        running_calc = running.Running()
        running_calc.weight = running.DEFAULT_WEIGHT[self.config.measurement_system]
        running_calc.distance = running.DEFAULT_DISTANCE[self.config.measurement_system]
        
        weightunits_calc = weightunits.WeightUnitsConverter()
        weightunits_calc.weight = weightunits.DEFAULT_WEIGHT[self.config.measurement_system]
        
        self.calculators = {'onerep_max' : onerep_max_calc,
                            'ideal_body' : idealbody_calc,
                            'bodyfat' : bodyfat_calc,
                            'body_mass_index' : bmi_calc,
                            'running' : running_calc,
                            'weightunits' : weightunits_calc}
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
