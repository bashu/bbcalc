# -*- coding: utf-8 -*-

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
from bbcalc.calculators.bodyfat import bodyfat_calc

from bbcalc.utils.unitconvertor import convert_length, convert_mass

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WAIST = (32.0, 81.5)
DEFAULT_WEIGHT = (220.0, 100.0)


class CustomModel(BaseModel):

    unit1_combobox = int()
    unit2_combobox = int()
    gender_combobox = int()
    waist_spinbutton = float()
    weight_spinbutton = float()
    percent_entry = float()
    fat_entry = float()
    lean_entry = float()
    calories_entry = float()
    result1_label = unicode()
    result2_label = unicode()
    result3_label = unicode()

    def calculation(self):
        if self.waist_spinbutton != 0 and self.weight_spinbutton != 0:
            return bodyfat_calc(self.waist_spinbutton,
                                self.weight_spinbutton,
                                self.unit1_combobox,
                                self.unit2_combobox,
                                self.gender_combobox)
        else:
            return None

    def set_unit1_combobox(self, value):
        self.waist_spinbutton = convert_length(self.waist_spinbutton, value)
        self.unit1_combobox = value

    def set_unit2_combobox(self, value):
        self.weight_spinbutton = convert_mass(self.weight_spinbutton, value)
        self.unit2_combobox = value

    def get_percent_entry(self):
        result = self.calculation()
        if result:
            return result['bodyfat']
        else:
            return self.percent_entry

    def get_fat_entry(self):
        result = self.calculation()
        if result:
            return result['fatweight']
        else:
            return self.fat_entry

    def get_lean_entry(self):
        result = self.calculation()
        if result:
            return result['lbm']
        else:
            return self.lean_entry

    def get_calories_entry(self):
        result = self.calculation()
        if result:
            return result['calories']
        else:
            return self.calories_entry
#    def get_result_entry(self):
#        if self.height_spinbutton != 0 and self.weight_spinbutton != 0:
#            result = bmi_calc(self.height_spinbutton,
#                              self.weight_spinbutton,
#                              self.unit1_combobox,
#                              self.unit2_combobox)
#            self.result_label = result['status']
#            return result['bmi']
#        else:
#            return self.result_entry
    def get_result1_label(self):
        return self.weight_abbr[self.unit2_combobox]

    def get_result2_label(self):
        return self.weight_abbr[self.unit2_combobox]

    def get_result3_label(self):
        result = self.calculation()
        if result:
            return result['classification']
        else:
            return unicode()

class Bodyfat(BaseClass):

    gladefile = 'bodyfat_window'
    model = CustomModel()
    widgets = ('waist_spinbutton',
               'weight_spinbutton',
               'percent_entry',
               'fat_entry',
               'lean_entry',
               'calories_entry',
               'result1_label',
               'result2_label',
               'result3_label',
               )
    proxy_widgets = ('unit1_combobox',
                     'unit2_combobox',
                     'gender_combobox',
                     'waist_spinbutton',
                     'weight_spinbutton',
                     'percent_entry',
                     'fat_entry',
                     'lean_entry',
                     'calories_entry',
                     'result1_label',
                     'result2_label',
                     'result3_label',
                     )
    measurement_system_widgets = ('unit1_combobox', 'unit2_combobox', )
    gender_widgets = ('gender_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit1_combobox.prefill([(value, key)
                for key, value in self.model.length_types.items()])
        self.model.waist_spinbutton = DEFAULT_WAIST[self.config.measurement_system]
        self.unit2_combobox.prefill([(value, key)
                for key, value in self.model.weight_types.items()])
        self.model.weight_spinbutton = DEFAULT_WEIGHT[self.config.measurement_system]
        self.gender_combobox.prefill([(value, key)
                for key, value in self.model.gender_types.items()])

    # Signal handlers

    def after_unit1_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_unit2_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_waist_spinbutton__changed(self, entry, *args):
        self.proxy.update_many(('percent_entry',
                                'fat_entry',
                                'lean_entry',
                                'calories_entry',
                                'result3_label', ))

    def after_weight_spinbutton__changed(self, entry, *args):
        self.proxy.update_many(('percent_entry',
                                'fat_entry',
                                'lean_entry',
                                'calories_entry',
                                'result3_label', ))

    def after_gender_combobox__changed(self, entry, *args):
        self.proxy.update_many(('percent_entry',
                                'fat_entry',
                                'lean_entry',
                                'calories_entry',
                                'result3_label', ))
