# -*- coding: utf-8 -*-

"""Initialization routines"""

import os, sys
import gtk
import gettext


def locations(self):
    """This function setup data locations"""
    # initialize all locations
    locations = {}
    locations['exec'] = sys.argv[0]

    # for Posix-like systems
    if os.name == 'posix':
        locations['bbcalc'] = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        locations['share'] = os.path.abspath(os.path.join(locations['bbcalc'], '..'))
        locations['glade'] = os.path.join(locations['bbcalc'], 'glade')
        locations['images'] = os.path.join(locations['bbcalc'], 'images')
        if os.path.isdir(os.path.join(locations['bbcalc'], 'i18n')):
            locations['locale'] = os.path.join(locations['bbcalc'], 'i18n')
        else:
            locations['locale'] = os.path.join(locations['share'], 'locale')
    # otherwise for Windows-like
    elif os.name == 'nt' or os.name == 'win32':
        locations['bbcalc'] = os.path.dirname(locations['exec'])
        locations['locale'] = os.path.join(locations['bbcalc'], 'i18n')
    self.locations = locations
    return locations
        
def i18n(location):
    """Set up i18n stuff"""
    gettext.bindtextdomain('bbcalc', location)
    gettext.textdomain('bbcalc')
    gtk.glade.bindtextdomain('bbcalc', location)
    gtk.glade.textdomain('bbcalc')
    
