# -*- coding: utf-8 -*-

import gconf

from bbcalc.utils import IMPERIAL, METRIC, MALE, FEMALE

# GConf directory for bbcalc
GCONF_DIR = '/apps/bbcalc'

# GConf default measurement system: Metric, Imperial
GCONF_MEASUREMENT_SYSTEM = '/measurement_system'

# GConf default gender: Male, Female
GCONF_DEFAULT_GENDER = '/default_gender'

# GConf variables
GCONF_GENDER_MALE = 'Male'
GCONF_GENDER_FEMALE = 'Female'

GCONF_SYSTEM_IMPERIAL = 'Imperial'
GCONF_SYSTEM_METRIC = 'Metric'


class Config(object):

	def __init__(self):
		self.client = gconf.client_get_default()
		self.client.add_dir(GCONF_DIR, gconf.CLIENT_PRELOAD_RECURSIVE)

	def __delattr__(self, name):
		"""Delete attributes method."""
		nodelete = ( 'measurement_system', 'default_gender' )

		if name in nodelete:
			raise TypeError, name + " property cannot be deleted"
		else:
			del self.__dict__[name]

	def __setattr__(self, name, value):
		"""Set attributes method."""
		if name == 'measurement_system':
			if value == IMPERIAL:
				self.set_string(GCONF_MEASUREMENT_SYSTEM, GCONF_SYSTEM_IMPERIAL)
			else:
				self.set_string(GCONF_MEASUREMENT_SYSTEM, GCONF_SYSTEM_METRIC)
		if name == 'default_gender':
			if value == MALE:
				self.set_string(GCONF_DEFAULT_GENDER, GCONF_GENDER_MALE)
			else:
				self.set_string(GCONF_DEFAULT_GENDER, GCONF_GENDER_FEMALE)
		else:
			self.__dict__[name] = value

	def __getattr__(self, name):
		"""Get attributes method."""
		if name == 'measurement_system':
			if self.get_string(GCONF_MEASUREMENT_SYSTEM) == GCONF_SYSTEM_IMPERIAL:
				return IMPERIAL
			else:
				return METRIC
		if name == 'default_gender':
			if self.get_string(GCONF_DEFAULT_GENDER) == GCONF_GENDER_MALE:
				return MALE
			else:
				return FEMALE
		else:
			return self.__dict__[name]

	def get_string(self, key):
		return self.client.get_string(GCONF_DIR + key)

	def set_string(self, key, value):
		self.client.set_string(GCONF_DIR + key, str(value))

	def notify_add(self, key, handler):
		return self.client.notify_add(GCONF_DIR + key, lambda x, y, z, a: handler(z.value))

	def notify_remove(self, notify):
		return self.client.notify_remove(notify)

