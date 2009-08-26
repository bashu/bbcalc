# -*- coding: utf-8 -*-

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
from bbcalc.calculators.running import running_calc

from bbcalc.utils.unitconvertor import convert_mass, convert_distance

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WEIGHT = (165.0, 75.0)
DEFAULT_DISTANCE = (15.0, 25.0)


class CustomModel(BaseModel):

    unit1_combobox = int()
    unit2_combobox = int()
    weight_spinbutton = float()
    distance_spinbutton = float()
    result_entry = float()

    def set_unit1_combobox(self, value):
        self.weight_spinbutton = convert_mass(self.weight_spinbutton, value)
        self.unit1_combobox = value

    def set_unit2_combobox(self, value):
        self.distance_spinbutton = convert_distance(self.distance_spinbutton, value)
        self.unit2_combobox = value

    def get_result_entry(self):
        if self.weight_spinbutton != 0 and self.distance_spinbutton != 0:
            return running_calc(self.weight_spinbutton,
                                self.distance_spinbutton,
                                self.unit1_combobox,
                                self.unit2_combobox)
        else:
            return self.result_entry


class Running(BaseClass):

    gladefile = 'running_window'
    model = CustomModel()
    widgets = ('weight_spinbutton',
               'distance_spinbutton',
               'result_entry', )
    proxy_widgets = ('weight_spinbutton',
                     'distance_spinbutton',
                     'result_entry',
                     'unit1_combobox',
                     'unit2_combobox', )
    measurement_system_widgets = ('unit1_combobox', 'unit2_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit1_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])
        self.model.weight_spinbutton = DEFAULT_WEIGHT[self.config.measurement_system]
        self.unit2_combobox.prefill([(value, key)
                for key, value in self.model.distance_types.items()])
        self.model.distance_spinbutton = DEFAULT_DISTANCE[self.config.measurement_system]

    # Signal handlers

    def after_unit1_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_unit2_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_weight_spinbutton__changed(self, entry, *args):
        self.proxy.update('result_entry')

    def after_distance_spinbutton__changed(self, entry, *args):
        self.proxy.update('result_entry')
