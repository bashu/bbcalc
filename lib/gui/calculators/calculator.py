# -*- coding: utf-8 -*-

"""
Generic class for all calculators

$Id$
"""

from lib.utils import METRIC, STR_KG, STR_LBS, STR_CM, STR_IN, STR_KM, STR_MI
from lib.utils.unitconvertor import kg2lb, lb2kg, in2cm, cm2in, km2mi, mi2km


class Calculator:

    mass_widgets = {}
    mass_labels = {}
    mass_units = {}
    
    length_widgets = {}
    length_labels = {}
    length_units = {}
    
    distance_widgets = {}
    distance_labels = {}
    distance_units = {}

    def unit_conversion(self, widgets, labels, units, metric, imperial, metric_str, imperial_str, key, value):
        """Generic method for unit conversion
        
        widgets - dictionary of input widgets,
        labels - dictionary of labels widgets,
        units - dictionary of units selection widgets,
        metric - function for imperial to metric conversion,
        imperial - function for metric to imperial conversion,
        metric_str - unicode string for metric,
        imperial_str - unicode string for imperial,
        key - unique key for widgets, labels and units,
        value - new value
        """
        try:
            if units[key] == value:
                return False
        except:
            return False
        units[key] = value
        try:
            for widget in widgets[key]:
                # Perform conversion for the mass value
                if units[key] == METRIC: 
                    widget.set_value(metric(widget.get_value()))
                else:
                    widget.set_value(imperial(widget.get_value()))
        except:
            pass
        try:
            for label in labels[key]:
                # Change label for the resulting unit type
                if units[key] != METRIC: 
                    label.set_text(imperial_str)
                else:
                    label.set_text(metric_str)
        except:
            pass

    def unit_conversion_mass(self, key, value):
        """Unit conversion for mass widgets"""
        self.unit_conversion(self.mass_widgets, self.mass_labels, self.mass_units, 
                             lb2kg, kg2lb, STR_KG, STR_LBS, key, value)

    def unit_conversion_length(self, key, value):
        """Unit conversion for length widgets"""
        self.unit_conversion(self.length_widgets, self.length_labels, self.length_units, 
                             in2cm, cm2in, STR_CM, STR_IN, key, value)

    def unit_conversion_distance(self, key, value):
        """Unit conversion for distance widgets"""
        self.unit_conversion(self.distance_widgets, self.distance_labels, self.distance_units, 
                             mi2km, km2mi, STR_KM, STR_MI, key, value)
