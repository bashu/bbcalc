## -*- coding: utf-8 -*-

from bbcalc.gui.calculators.baseclass import BaseModel, BaseClass
from bbcalc.calculators.idealbody import ideal_body_calc

from bbcalc.utils.unitconvertor import convert_length

# Predefined values, used somewhere else. [0] - Imperial, [1] - Metric
DEFAULT_WRIST = (6.89, 17.5)


class CustomModel(BaseModel):

    wrist_spinbutton = float()
    unit_combobox = int()
    chest_entry = float()
    hip_entry = float()
    waist_entry = float()
    thigh_entry = float()
    neck_entry = float()
    bicep_entry = float()
    calve_entry = float()
    forearm_entry = float()

    # List of result entries
    result_entries = ['wrist_spinbutton',
                      'chest_entry',
                      'hip_entry',
                      'waist_entry',
                      'thigh_entry',
                      'neck_entry',
                      'bicep_entry',
                      'calve_entry',
                      'forearm_entry']

    def set_unit_combobox(self, value):
        self.wrist_spinbutton = convert_length(self.wrist_spinbutton, value)
        self.unit_combobox = value

    def set_wrist_spinbutton(self, value):
        self.wrist_spinbutton = value
        # Result calculation
        results = ideal_body_calc(value, precision=1)

        for idx in xrange(1, len(self.result_entries)):
            if hasattr(self, self.result_entries[idx]):
                setattr(self, self.result_entries[idx], results[idx])


class IdealBody(BaseClass):

    gladefile = 'ideal_body_window'
    model = CustomModel()
    widgets = ('wrist_spinbutton',
               'chest_entry',
               'waist_entry',
               'hip_entry',
               'bicep_entry',
               'forearm_entry',
               'thigh_entry',
               'calve_entry',
               'neck_entry' )
    proxy_widgets = ('unit_combobox',
                     'wrist_spinbutton',
                     'chest_entry',
                     'waist_entry',
                     'hip_entry',
                     'bicep_entry',
                     'forearm_entry',
                     'thigh_entry',
                     'calve_entry',
                     'neck_entry' )
    measurement_system_widgets = ('unit_combobox', )

    def __init__(self):
        BaseClass.__init__(self)

    def _setup_widgets(self):
        self.unit_combobox.prefill([(value, key)
                for key, value in self.model.length_types.items()])
        self.model.wrist_spinbutton = DEFAULT_WRIST[self.config.measurement_system]

    # Signal handlers

    def after_unit_combobox__changed(self, entry, *args):
        self.proxy.update_many((self.widgets))

    def after_wrist_spinbutton__changed(self, entry, *args):
        self.proxy.update_many(('chest_entry',
                                'waist_entry',
                                'hip_entry',
                                'bicep_entry',
                                'forearm_entry',
                                'thigh_entry',
                                'calve_entry',
                                'neck_entry'))
