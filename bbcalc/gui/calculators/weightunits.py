# -*- coding: utf-8 -*-

import gconf

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
import bbcalc.utils.config as config

from bbcalc.utils.unitconvertor import convert_mass
from bbcalc.utils import IMPERIAL, METRIC


# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (165.0, 75.0)

class CustomModel(BaseModel):

    unit1_combobox = int()
    unit2_combobox = int()
    weight_spinbutton = float()
    result_entry = float()

    def set_unit1_combobox(self, value):
        self.weight_spinbutton = convert_mass(self.weight_spinbutton, value)
        self.unit1_combobox = value

    def get_result_entry(self):
        if self.unit1_combobox != self.unit2_combobox:
            return convert_mass(self.weight_spinbutton, self.unit2_combobox)
        else:
            return self.weight_spinbutton
#
#    def get_result_label(self):
#        return self.weight_abbr[self.unit_combobox]

class WeightUnitsConverter(BaseClass):

    gladefile = 'weightunits_window'
    model = CustomModel()
    widgets = ('result_entry',
               'weight_spinbutton', )
    proxy_widgets = ('result_entry',
                     'unit1_combobox',
                     'unit2_combobox',
                     'weight_spinbutton', )
    measurement_system_widgets = ('unit1_combobox', 'unit2_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit1_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])
        self.model.weight_spinbutton = DEFAULT_WEIGHT[self.config.measurement_system]
        self.unit2_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])

    def _load_gconf_defaults(self):
        """Load GConf defaults"""
        # Set active item for unit selection box
        if self.config.measurement_system == IMPERIAL:
            self.model.unit1_combobox = IMPERIAL
            self.model.unit2_combobox = METRIC
        else:
            self.model.unit1_combobox = METRIC
            self.model.unit2_combobox = IMPERIAL

    # Signal handlers

    def after_unit1_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_unit2_combobox__changed(self, entry, *args):
        self.proxy.update('result_entry')

    def after_weight_spinbutton__changed(self, entry, *args):
        self.proxy.update('result_entry')

    def on_gconf_changed(self, value):
        if value is None or value.type != gconf.VALUE_STRING:
            return
        if value.get_string() == config.GCONF_SYSTEM_IMPERIAL:
            self.model.unit1_combobox = IMPERIAL
            self.model.unit2_combobox = METRIC
        if value.get_string() == config.GCONF_SYSTEM_METRIC:
            self.model.unit1_combobox = METRIC
            self.model.unit2_combobox = IMPERIAL
