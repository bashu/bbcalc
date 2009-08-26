# -*- coding: utf-8 -*-

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
from bbcalc.calculators.bmi import bmi_calc

from bbcalc.utils.unitconvertor import convert_length, convert_mass

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_HEIGHT = (73.0, 185.0)
DEFAULT_WEIGHT = (165.0, 75.0)


class CustomModel(BaseModel):

    unit1_combobox = int()
    unit2_combobox = int()
    height_spinbutton = float()
    weight_spinbutton = float()
    result_entry = float()
    result_label = unicode()

    def set_unit1_combobox(self, value):
        self.height_spinbutton = convert_length(self.height_spinbutton, value)
        self.unit1_combobox = value

    def set_unit2_combobox(self, value):
        self.weight_spinbutton = convert_mass(self.weight_spinbutton, value)
        self.unit2_combobox = value

    def get_result_entry(self):
        if self.height_spinbutton != 0 and self.weight_spinbutton != 0:
            result = bmi_calc(self.height_spinbutton,
                              self.weight_spinbutton,
                              self.unit1_combobox,
                              self.unit2_combobox)
            self.result_label = result['status']
            return result['bmi']
        else:
            return self.result_entry


class BMI(BaseClass):

    gladefile = 'bmi_window'
    model = CustomModel()
    widgets = ('height_spinbutton',
               'weight_spinbutton',
               'result_entry',
               'result_label', )
    proxy_widgets = ('unit1_combobox',
                     'unit2_combobox',
                     'height_spinbutton',
                     'weight_spinbutton',
                     'result_entry',
                     'result_label', )
    measurement_system_widgets = ('unit1_combobox', 'unit2_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit1_combobox.prefill([(value, key)
                for key, value in self.model.length_types.items()])
        self.model.height_spinbutton = DEFAULT_HEIGHT[self.config.measurement_system]
        self.unit2_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])
        self.model.weight_spinbutton = DEFAULT_WEIGHT[self.config.measurement_system]

    # Signal handlers

    def after_unit1_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_unit2_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_height_spinbutton__changed(self, entry, *args):
        self.proxy.update_many(('result_entry', 'result_label'))

    def after_weight_spinbutton__changed(self, entry, *args):
        self.proxy.update_many(('result_entry', 'result_label'))
