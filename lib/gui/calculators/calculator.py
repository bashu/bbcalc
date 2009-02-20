# -*- coding: utf-8 -*-

"""
Generic class for all calculators

$Id$
"""

from lib.utils import METRIC, STR_KG, STR_LBS, STR_CM, STR_IN, STR_KM, STR_MI
from lib.utils.unitconvertor import kg2lb, lb2kg, in2cm, cm2in, km2mi, mi2km


class Calculator:
    # TODO: Refactore this class
    
    mass_widgets = {}
    mass_labels = {}
    mass_units = {}
    
    length_widgets = {}
    length_labels = {}
    length_units = {}
    
    distance_widgets = {}
    distance_labels = {}
    distance_units = {}
    
    def unit_conversion_mass(self, key, value):
        """Unit conversion for mass widgets"""
        try:
            if self.mass_units[key] == value:
                return False
        except:
            return False
        self.mass_units[key] = value
        try:
            for widget in self.mass_widgets[key]:
                # Perform conversion for the mass value
                if self.mass_units[key] == METRIC: 
                    widget.set_value(lb2kg(widget.get_value()))
                else:
                    widget.set_value(kg2lb(widget.get_value()))
        except:
            pass
        try:
            for label in self.mass_labels[key]:
                # Change label for the resulting unit type
                if self.mass_units[key] != METRIC: 
                    label.set_text(STR_LBS)
                else:
                    label.set_text(STR_KG)
        except:
            pass

    def unit_conversion_length(self, key, value):
        """Unit conversion for length widgets"""
        try:
            if self.length_units[key] == value:
                return False
        except:
            return False
        self.length_units[key] = value
        try:
            for widget in self.length_widgets[key]:
                # Perform conversion for the length value
                if self.length_units[key] == METRIC:
                    widget.set_value(in2cm(widget.get_value()))
                else:
                    widget.set_value(cm2in(widget.get_value()))
        except:
            pass
        try:
            for label in self.length_labels[key]:
                # Change label for the resulting unit type
                if self.length_units[key] != METRIC: 
                    label.set_text(STR_IN)
                else: 
                    label.set_text(STR_CM)
        except:
            pass

    def unit_conversion_distance(self, key, value):
        """Unit conversion for distance widgets"""
        try:
            if self.distance_units[key] == value:
                return False
        except:
            return False
        self.distance_units[key] = value
        try:
            for widget in self.distance_widgets[key]:
                # Perform conversion for the distance value
                if self.distance_units[key] == METRIC: 
                    widget.set_value(mi2km(widget.get_value()))
                else:
                    widget.set_value(km2mi(widget.get_value()))
        except:
            pass
        try:
            for label in self.distance_labels[key]:
                # Change label for the resulting unit type
                if self.distance_units[key] != METRIC: 
                    label.set_text(STR_MI)
                else:
                    label.set_text(STR_KM)
        except:
            pass