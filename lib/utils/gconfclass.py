# -*- coding: utf-8 -*-

"""
Utility class for working with gconf

$Id$
"""

from lib import GCONF_CLIENT


class GConf(object):
	
	def notify_add(self, key, handler):
		return GCONF_CLIENT.notify_add(key, lambda x, y, z, a: handler(z.value))