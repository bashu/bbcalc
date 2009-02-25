# -*- coding: utf-8 -*-

"""
Miscellaneous unit converters

$Id$
"""

from lib.utils import POUNDS, INCHES, MILES

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
