# -*- coding: utf-8 -*-

"""
Initialization routines

$Id$
"""

import gtk
import gettext


def init_i18n(directory):
    """Enable i18n"""
    gettext.bindtextdomain('bbcalc', directory)
    gettext.textdomain('bbcalc')
    gtk.glade.bindtextdomain('bbcalc', directory)
    gtk.glade.textdomain('bbcalc')
    
