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

# Get dictionary of data locations
from lib.initialize import locations


class MainApp:
    """Create application based on a MainFrame class"""

    def __init__(self):
		
        # Set the Glade file
        self.gladefile = os.path.join(locations['glade'], 'mainwindow.glade')  
        self.xml = gtk.glade.XML(self.gladefile) 
		
        signals = {}
        for key in dir(self.__class__):
            signals[key] = getattr(self, key)
        self.xml.signal_autoconnect(signals)

    def app_quit(self, *args):
        gtk.main_quit()

    def on_main_window_destroy(self, *args):
        self.app_quit(args)

    def on_quit1_activate(self, *args):
        self.app_quit(args)

    def on_about1_activate(self, *args):
        from lib.gui.about import AboutDialog
        about_dialog = AboutDialog()


def main():
    app = MainApp()
    gtk.main()
