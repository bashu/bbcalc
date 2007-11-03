# -*- coding: utf-8 -*-

"""Miscellaneous unit convertors"""

from lib.gui.utils import *

def kg2lb(kg, precision=5):
    """Convert kilogramms to pounds"""
    return round(kg * POUNDS, precision)

def lb2kg(lb, precision=5):
    """Convert pounds to kilogramms"""
    return round(lb / POUNDS, precision)

def cm2in(cm, precision=5):
    return round(cm / INCHES, precision)

def in2cm(inches, precision=5):
    return round(inches * INCHES, precision)