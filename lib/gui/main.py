# -*- coding: utf-8 -*-

"""
Main Application class

$Id
"""

# GTK stuff
try:
    import pygtk
    pygtk.require("2.0")
except:
    pass
try:
    import gtk
    import gtk.glade
except:
    import sys
    sys.exit(1)

import os.path
from lib import GLADE_DIR

GLADE_FILE = os.path.join(GLADE_DIR, 'bbcalc.glade')

from lib.gui.glade import Component

from lib.gui.calculators.idealbody import IdealBody
from lib.gui.calculators.onerepmax import OneRepMax
from lib.gui.calculators.bodyfat import Bodyfat


class MainApp(Component):
    """Create application based on a MainFrame class"""

    def __init__(self):
        Component.__init__(self, GLADE_FILE, 'main_window')

        # Create calculators tables
        self.onerepmax = OneRepMax()
        self.idealbody = IdealBody()
        self.bodyfat = Bodyfat()
        # Set default panel
        self.set_panel(self.idealbody)

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
        # Set statusbar text for selected calculator
        self.statusbar.push(-1, panel.description)

    def on_main_window_destroy(self, *args):
        self.app_quit(args)

    def on_quit_activate(self, *args):
        self.app_quit(args)

    def on_preferences_activate(self, *args):
        """Shows Preferences dialog box"""
        from lib.gui.preferences import PreferencesDialog
        prefs_dialog = PreferencesDialog()

    def on_about_activate(self, *args):
        """Shows About dialog box"""
        from lib.gui.about import AboutDialog
        about_dialog = AboutDialog()

    def on_ideal_body_activate(self, widget):
        """Shows Ideal Body Measurements"""
        if widget.get_active() == True:
            self.set_panel(self.idealbody)
        
    def on_bodyfat_activate(self, widget):
        """Shows Bodyfat Estimator"""
        if widget.get_active() == True:
            self.set_panel(self.bodyfat)

    def on_onerep_max_activate(self, widget):
        """Shows One Rep Max calculator"""
        if widget.get_active() == True:
            self.set_panel(self.onerepmax)


def main():
    app = MainApp()
    gtk.main()
