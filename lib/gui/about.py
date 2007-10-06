# -*- coding: utf-8 -*-

from gettext import gettext as _
import gtk
import os
import sys

import lib.version as version


class AboutDialog:
    """Shows a gtk about dialog"""

    def __init__(self):
        dialog = gtk.AboutDialog()
        dialog.set_name(version.pname)
        dialog.set_version(version.pversion)
        dialog.set_copyright("Copyright © 2005-2007 Basil Shubin")
        dialog.set_website(version.pwebsite)
        dialog.set_authors([version.pauthor.replace(', ', '\n')])

        if os.path.isfile('/usr/share/common-licenses/GPL-3'):
            dialog.set_license(open('/usr/share/common-licenses/GPL-3').read())
        else:
            dialog.set_license(license_text)
        dialog.set_comments(version.pdescription)
        dialog.run()
        dialog.destroy()

# license text of this appp    
license_text = """BBCalc is free software; you can redistribute it and/or modify 
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
"""
