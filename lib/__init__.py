# This file is necessary to make this directory a package.

import os
import gtk.glade, gconf
import gettext

from lib.utils import IMPERIAL, METRIC, MALE, FEMALE


APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

SHARE_DIR = os.path.abspath(os.path.join(APP_DIR, '..'))

GLADE_DIR = os.path.join(APP_DIR, 'glade')

IMAGES_DIR = os.path.join(APP_DIR, 'images')

if os.path.isdir(os.path.join(APP_DIR, 'i18n')):
    LOCALE_DIR = os.path.join(APP_DIR, 'i18n')
else:
    LOCALE_DIR = os.path.join(SHARE_DIR, 'locale')


# Enable i18n
gettext.bindtextdomain('bbcalc', LOCALE_DIR)
gettext.textdomain('bbcalc')
gtk.glade.bindtextdomain('bbcalc', LOCALE_DIR)
gtk.glade.textdomain('bbcalc')


# BBCalc help file
HELP_CONTENTS = 'bbcalc.xml'

