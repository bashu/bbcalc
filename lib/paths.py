# -*- coding: utf-8 -*-

"""
Miscellaneous directories

$Id$
"""

import os

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

share_dir = os.path.abspath(os.path.join(app_dir, '..'))

glade_dir = os.path.join(app_dir, 'glade')

images_dir = os.path.join(app_dir, 'images')

if os.path.isdir(os.path.join(app_dir, 'i18n')):
    locale_dir = os.path.join(app_dir, 'i18n')
else:
    locale_dir = os.path.join(share_dir, 'locale')
