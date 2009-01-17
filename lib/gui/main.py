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

import lib.initialize as initialize

from lib.gui.calculators.idealbody import IdealBody
from lib.gui.calculators.onerepmax import OneRepMax
from lib.gui.calculators.bodyfat import Bodyfat


class MainApp:
    """Create application based on a MainFrame class"""

    def __init__(self):

        # Initialize data directories, e.g. path to images and etc
        self.directories = initialize.init_dir()
        # Initialize locale and i18n
        initialize.init_i18n(self.directories['locale'])
        
        # Set the Glade file
        self.gladefile = os.path.join(self.directories['glade'], 'bbcalc.glade')  
        self.xml = gtk.glade.XML(self.gladefile)

        # Get main window and hide it, until all we create all widgets
        self.main_window = self.xml.get_widget('main_window')
        self.main_window.hide()

        # Get a box for a future calculators
        self.calc_box = self.xml.get_widget('calc_box')

        # Get statusbar
        self.statusbar = self.xml.get_widget('statusbar1')

        # Create calculators tables
        self.onerepmax = OneRepMax(self)
        self.idealbody = IdealBody(self)
        self.bodyfat = Bodyfat(self)
        # Set default panel
        self.set_panel(self.idealbody)

        # Connect event handlers
        signals = {}
        for key in dir(self.__class__):
            signals[key] = getattr(self, key)
        self.xml.signal_autoconnect(signals)

        # Show main window and goes to main loop
        self.main_window.show()

    def app_quit(self, *args):
        """Quits application"""
        gtk.main_quit()

    def set_panel(self, panel):
        """Set working panel"""
        if hasattr(self, 'panel'):
            self.panel.calc_table.reparent(self.panel.old_parent)
        self.panel = panel
        self.panel.calc_table.reparent(self.calc_box)
        # Set statusbar text for selected calculator
        self.statusbar.push(-1, panel.description)

    def on_main_window_destroy(self, *args):
        self.app_quit(args)

    def on_quit_activate(self, *args):
        self.app_quit(args)

    def on_about_activate(self, *args):
        """Shows About dialog box"""
        from lib.gui.about import AboutDialog
        about_dialog = AboutDialog(self.directories['images'])

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
