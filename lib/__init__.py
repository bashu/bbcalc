# This file is necessary to make this directory a package.

import os
import gtk.glade, gconf
import gettext


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


#Gconf client
GCONF_CLIENT = gconf.client_get_default()

# GConf directory for bbcalc
GCONF_DIR = '/apps/bbcalc'

# GConf default measurement system: Metric, Imperial
GCONF_MEASUREMENT_SYSTEM = GCONF_DIR + '/measurement_system'

# GConf default gender: Male, Female
GCONF_DEFAULT_GENDER = GCONF_DIR + '/default_gender'

# GConf variables
GCONF_GENDER_MALE = 'Male'
GCONF_GENDER_FEMALE = 'Female'

GCONF_SYSTEM_METRIC = 'Metric'
GCONF_SYSTEM_IMPERIAL = 'Imperial'

# Preload gconf directories
GCONF_CLIENT.add_dir(GCONF_DIR, gconf.CLIENT_PRELOAD_RECURSIVE)

# Set up default system of measurements
DEFAULT_MEASUREMENT_SYSTEM = GCONF_CLIENT.get_string(GCONF_MEASUREMENT_SYSTEM)

# Set up default gender
DEFAULT_GENDER = GCONF_CLIENT.get_string(GCONF_DEFAULT_GENDER)

# BBCalc help file
HELP_CONTENTS = 'bbcalc.xml'

