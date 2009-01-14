# -*- coding: utf-8 -*-

"""
Miscellaneous unit converters

$Id$
"""

from lib.utils import POUNDS, INCHES

def kg2lb(kg, precision=5):
    """Convert kilogramms to pounds"""
    return round(kg * POUNDS, precision)

def lb2kg(lb, precision=5):
    """Convert pounds to kilogramms"""
    return round(lb / POUNDS, precision)

def cm2in(cm, precision=5):
    """Convert centimeters to inches"""
    return round(cm / INCHES, precision)

def in2cm(inches, precision=5):
    """Convert inches to centimeters"""
    return round(inches * INCHES, precision)
