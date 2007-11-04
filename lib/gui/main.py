# -*- coding: utf-8 -*-

"""Application class"""

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


class MainApp:
    """Create application based on a MainFrame class"""

    def __init__(self):

        initialize.locations(self)
        initialize.i18n(self.locations['locale'])
        
        # Set the Glade file
        self.gladefile = os.path.join(self.locations['glade'], 'mainwindow.glade')  
        self.xml = gtk.glade.XML(self.gladefile)

        # Get a box for a future calcs
        self.calc_box = self.xml.get_widget('calc_box')

        # Create calcs tables
        self.onerepmax = OneRepMax(self)
        self.idealbody = IdealBody(self)

        self.set_panel(self.idealbody)

        signals = {}
        for key in dir(self.__class__):
            signals[key] = getattr(self, key)
        self.xml.signal_autoconnect(signals)

    def app_quit(self, *args):
        gtk.main_quit()

    def set_panel(self, panel):
        if hasattr(self, 'panel'):
            self.panel.calc_table.reparent(self.panel.old_parent)
        self.panel = panel
        self.panel.calc_table.reparent(self.calc_box)

    def on_main_window_destroy(self, *args):
        self.app_quit(args)

    def on_quit_activate(self, *args):
        self.app_quit(args)

    def on_about_activate(self, *args):
        """Shows About dialog box"""
        from lib.gui.about import AboutDialog
        about_dialog = AboutDialog()

    def on_ideal_body_activate(self, widget):
        if widget.get_active() == True:
            self.set_panel(self.idealbody)
        
    def on_bodyfat_activate(self, *args):
        pass

    def on_onerep_max_activate(self, widget):
        if widget.get_active() == True:
            self.set_panel(self.onerepmax)


def main():
    app = MainApp()
    gtk.main()
