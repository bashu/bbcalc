# -*- coding: utf-8 -*-

"""
Initialization routines

$Id$
"""

import gtk
import gettext


#def init_dir():
#    """Working directories"""
#    directories = {}
#    directories['exec'] = sys.argv[0]
#
#    # for Posix-like systems
#    if os.name == 'posix':
#        directories['bbcalc'] = \
#            os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
#        directories['share'] = \
#            os.path.abspath(os.path.join(directories['bbcalc'], '..'))
#        directories['glade'] = os.path.join(directories['bbcalc'], 'glade')
#        directories['images'] = os.path.join(directories['bbcalc'], 'images')
#        if os.path.isdir(os.path.join(directories['bbcalc'], 'i18n')):
#            directories['locale'] = os.path.join(directories['bbcalc'], 'i18n')
#        else:
#            directories['locale'] = os.path.join(directories['share'], 'locale')
#    # otherwise for Windows-like
#    elif os.name == 'nt' or os.name == 'win32':
#        directories['bbcalc'] = os.path.dirname(directories['exec'])
#        directories['locale'] = os.path.join(directories['bbcalc'], 'i18n')
#    return directories
        
def init_i18n(directory):
    """Enable i18n"""
    gettext.bindtextdomain('bbcalc', directory)
    gettext.textdomain('bbcalc')
    gtk.glade.bindtextdomain('bbcalc', directory)
    gtk.glade.textdomain('bbcalc')
    
