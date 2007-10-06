# -*- coding: utf-8 -*-

"""Initialization routines"""

import os
import re

# dictionary for data locations
locations = dict()

def initialize(app_path):
    """Initialization metafunction"""
   
    init_locations(app_path)

def init_locations(app_path):
	"""This function setup data locations"""
	# initialize all locations
	locations['exec'] = app_path

	# for Posix-like systems
	if os.name == 'posix':
		locations['bbcalc'] = os.path.join(os.path.dirname(__file__), '..')
		locations['share'] = os.path.join(locations['bbcalc'], '..')
		locations['glade'] = os.path.join(locations['bbcalc'], 'glade')
        # XXX: Replace with new locales
		#if os.path.isdir(os.path.join(locations['bbcalc'], 'i18n')):
		#	locations['locale'] = os.path.join(locations['bbcalc'], 'i18n')
		#else:
		#	locations['locale'] = os.path.join(locations['share'], 'locale')
	# otherwise for Windows-like
	elif os.name == 'nt' or os.name == 'win32':
		locations['bbcalc'] = os.path.dirname(locations['exec'])
        # XXX: Reaplace with new locales
		#locations['locale'] = os.path.join(locations['bbcalc'], 'i18n')
        
def init_i18n():
    """Set up i18n stuff"""
	# XXX: replace this with code for PyGTK
    global _wxloc
    wx.Locale.AddCatalogLookupPathPrefix(locations['locale'])
    _wxloc = wx.Locale(wx.LANGUAGE_DEFAULT)
    _wxloc.AddCatalog('bbcalc')
    import __builtin__
    setattr(__builtin__, '_', wx.GetTranslation)
    
