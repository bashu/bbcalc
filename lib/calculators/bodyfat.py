# -*- coding: utf-8 -*-

"""
Body Fat calculator.

This formula comes from 'The Bodyfat Guide' by Ron Brown

$Id$
"""

from lib.utils import KILOGRAMMS, POUNDS, MALE, FEMALE
from lib.utils import METRIC

from lib.utils.unitconvertor import kg2lb, cm2in

# General constants
MALECOEF = 98.42
FEMALECOEF = 76.76

WAISTCOEF = 4.15
WEIGHTCOEF = 1.082

CALORIESCOEF = 13.83

def bodyfat_calc(waist, weight, waist_unit=METRIC, weight_unit=METRIC, gender=MALE, precision=2):
    if waist_unit == METRIC:
        waist = cm2in(float(waist))
    if weight_unit == METRIC:
        weight = kg2lb(float(weight))
    tmp_waist = float(waist) * WAISTCOEF
    tmp_weight = float(weight) * WEIGHTCOEF
    diff = tmp_weight - tmp_waist;
    if gender == FEMALE:
        lbm = diff + FEMALECOEF;
    else:
        lbm = diff + MALECOEF;
    fatweight = float(weight) - lbm;
    bodyfat = fatweight / float(weight) * 100.0;
    if weight_unit == METRIC:
        factor = POUNDS
    else:
        factor = KILOGRAMMS

    bodyfat = round(bodyfat, precision)
    fatweight = round(fatweight / factor, precision)
    lbm = round(lbm / factor, precision)
    calories = round(lbm * CALORIESCOEF, 0)

    return {'bodyfat' : bodyfat, 'fatweight' : fatweight, 'lbm' : lbm, 
            'calories' : calories}

