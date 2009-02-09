# -*- coding: utf-8 -*-

"""
Utility class for working with glade files

Copyright (c) 2002-2008 Stephen Kennedy <stevek@gnome.org>

$Id$
"""

import gtk.glade


class Component(object):
    """Base class for all glade objects.

    This class handles loading the xml glade file and autoconnects
    all signals in the glade file.

    The handle to the xml file is stored in 'self.xml'. The
    toplevel widget is stored in 'self.widget'.

    In addition it calls widget.set_data("pyobject", self) - this
    allows us to get the python object given only the 'raw' gtk+
    object, which is sadly sometimes necessary.
    """

    def __init__(self, filename, root, override={}):
        """Load the widgets from the node 'root' in file 'filename'"""
        self.xml = gtk.glade.XML(filename, root, typedict=override)
        self.xml.signal_autoconnect(self)
        self.widget = getattr(self, root)
        self.widget.set_data('pyobject', self)

    def __getattr__(self, key):
        """Allow glade widgets to be accessed as self.widgetname"""
        widget = self.xml.get_widget(key)
        if widget: # cache lookups
            setattr(self, key, widget)
            return widget
        raise AttributeError(key)
