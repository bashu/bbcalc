# -*- coding: utf-8 -*-

from gettext import gettext as _

APP_NAME        = u'BBCalc'
APP_VERSION     = u'0.8.1'
# List of authors
APP_AUTHORS     = [u'Basil Shubin <bashu@users.sourceforge.net>']
APP_YEAR        = u'2005-2009'
APP_WEBSITE     = u'http://bbcalc.sf.net/'
APP_COPYRIGHT   = _(u"Copyright © %s Basil Shubin") % (APP_YEAR)

APP_DESCRIPTION = _(u"""BBCalc (Body Building Calculators) is a set of calculators
related to body building and fitness topics.""")

# license text of this application
APP_LICENSE     = _(u"""BBCalc is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

BBCalc is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with GnomeBaker; if not, write to the Free Software Foundation, Inc.,
59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
""")

try:
    from kiwi.environ import Application
except ImportError:
    raise SystemExit("Could not find kiwi")

app = Application(APP_NAME.lower())
if app.uninstalled:
    app.add_global_resource('pixmaps', 'data/pixmaps')
    app.add_global_resource('glade', 'data/glade')
app.enable_translation()
app.set_application_domain(APP_NAME.lower())