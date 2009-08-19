# -*- coding: utf-8 -*-

import gtk
import os

from kiwi.environ import environ
import bbcalc


def about_dialog(*args):
    """Run about dialog"""
    about = gtk.AboutDialog()
    # Set general info: version, authors and etc
    about.set_name(bbcalc.APP_NAME)
    about.set_version(bbcalc.APP_VERSION)
    about.set_copyright(bbcalc.APP_COPYRIGHT)
    about.set_website(bbcalc.APP_WEBSITE)
    about.set_authors([author + '\n' for author in bbcalc.APP_AUTHORS])

    # Loading app logo
    icon_file = environ.find_resource('pixmaps', 'bbcalc_logo.png')
    logo = gtk.gdk.pixbuf_new_from_file(icon_file)
    about.set_logo(logo)

    # Set app license text
    if os.path.isfile('/usr/share/common-licenses/GPL-3'):
        about.set_license(open('/usr/share/common-licenses/GPL-3').read())
    else:
        about.set_license(bbcalc.APP_LICENSE)
    about.set_comments(bbcalc.APP_DESCRIPTION)

    about.run()
    about.destroy()

