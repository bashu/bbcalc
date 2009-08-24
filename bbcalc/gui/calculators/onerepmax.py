# -*- coding: utf-8 -*-

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
from bbcalc.calculators.onerepmax import onerep_max_calc

from bbcalc.utils.unitconvertor import convert_mass

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (220.0, 100.0)


class CustomModel(BaseModel):

    weight_spinbutton = float()
    reps_spinbutton = 8
    unit_combobox = int()
    result_entry = float()
    result_label = unicode()

    def set_unit_combobox(self, value):
        self.weight_spinbutton = convert_mass(self.weight_spinbutton, value)
        self.unit_combobox = value

    def get_result_entry(self):
        return onerep_max_calc(self.weight_spinbutton, self.reps_spinbutton)

    def get_result_label(self):
        return self.weight_abbr[self.unit_combobox]


class OneRepMax(BaseClass):

    gladefile = 'one_rep_max_window'
    model = CustomModel()
    widgets = ('result_entry', 'result_label', 'weight_spinbutton', )
    proxy_widgets = ('result_entry', 'result_label', 'unit_combobox', 'weight_spinbutton', 'reps_spinbutton', )
    measurement_system_widgets = ('unit_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])
        self.model.weight_spinbutton = DEFAULT_WEIGHT[self.config.measurement_system]

    # Signal handlers

    def after_unit_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_weight_spinbutton__changed(self, entry, *args):
        self.proxy.update('result_entry')

    def after_reps_spinbutton__changed(self, entry, *args):
        self.proxy.update('result_entry')
