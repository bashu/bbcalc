import gconf

from gettext import gettext as _
from kiwi.ui.delegates import ProxySlaveDelegate

import bbcalc.utils.config as config
from bbcalc.utils import METRIC, IMPERIAL


class BaseModel(object):
    # Predefined types
    weight_types = {IMPERIAL : _(u'Pounds'),
                    METRIC : _(u'Kilograms')}

    length_types = {IMPERIAL : _(u'Inches'),
                    METRIC : _(u'Centimeters')}

    distance_types = {IMPERIAL : _(u'Miles'),
                    METRIC : _(u'Kilometers')}

    weight_abbr = {IMPERIAL : _(u'lbs'),
                   METRIC : _(u'kg')}

    length_abbr = {IMPERIAL : _(u'in'),
                   METRIC : _(u'cm')}

    distance_abbr = {IMPERIAL : _(u'mi'),
                   METRIC : _(u'km')}


class BaseClass(ProxySlaveDelegate):

    gladefile = None
    model = BaseModel()
    proxy_widgets = []
    measurement_system_widgets = [] # measurement system selection widgets
    gender_widgets = [] # gender selection widgets

    def __init__(self):
        ProxySlaveDelegate.__init__(self, self.model)
        self.config = config.Config()

        # Loading default values from GConf
        self._load_gconf_defaults()
        # Creating GConf notification handlers
        self._setup_gconf_notification()

        # Setting widgets
        self._setup_widgets()
        # Setting proxy
        self._setup_proxy()

    def _update_defaults(self, widgets=[], value=None):
        for widget_name in widgets:
            if hasattr(self.model, widget_name):
                setattr(self.model, widget_name, value)

    def _load_gconf_defaults(self):
        """Load GConf defaults"""
        # Set active item for measurement system selection widgets
        self._update_defaults(self.measurement_system_widgets,
                              self.config.measurement_system)

    def _setup_gconf_notification(self):
        """Bind GConf notification handlers"""
        self.config.notify_add(config.GCONF_MEASUREMENT_SYSTEM, self.on_gconf_changed)
        self.config.notify_add(config.GCONF_DEFAULT_GENDER, self.on_gconf_changed)

    def _setup_proxy(self):
        self.proxy = self.add_proxy(self.model, self.proxy_widgets)

    def _setup_widgets(self):
        # Must be overridden in a descendant class
        # Set default value(s) here
        pass

    # Signal handlers

    def on_gconf_changed(self, value):
        """Handle unit conversion"""
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL or \
                value.get_string() == config.GCONF_SYSTEM_METRIC:
            self._update_defaults(self.measurement_system_widgets,
                                  self.config.measurement_system)
