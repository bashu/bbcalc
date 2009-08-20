# -*- coding: utf-8 -*-

from bbcalc.utils import POUNDS, INCHES, MILES
from bbcalc.utils import IMPERIAL, METRIC

def kg2lb(kg, precision=2):
    """Convert kilograms to pounds"""
    return round(kg * POUNDS, precision)

def lb2kg(lb, precision=2):
    """Convert pounds to kilograms"""
    return round(lb / POUNDS, precision)

def cm2in(cm, precision=2):
    """Convert centimeters to inches"""
    return round(cm / INCHES, precision)

def in2cm(inches, precision=2):
    """Convert inches to centimeters"""
    return round(inches * INCHES, precision)

def km2mi(km, precision=2):
    """Convert kilometers to miles"""
    return round(km / MILES, precision)

def mi2km(miles, precision=2):
    """Convert miles to kilometers"""
    return round(miles * MILES, precision)

def convert_mass(value, system=METRIC, precision=2):
    """Convert mass from one measurement system to another"""
    if system == METRIC:
        return lb2kg(value, precision)
    elif system == IMPERIAL:
        return kg2lb(value, precision)
    else:
        return None

def convert_length(value, system=METRIC, precision=2):
    """Convert length from one measurement system to another"""
    if system == METRIC:
        return in2cm(value, precision)
    elif system == IMPERIAL:
        return cm2in(value, precision)
    else:
        return None
