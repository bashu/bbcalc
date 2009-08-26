# -*- coding: utf-8 -*-

from gettext import gettext as _

from bbcalc.utils import KILOGRAMS, POUNDS, MALE, FEMALE, METRIC
from bbcalc.utils.unitconvertor import kg2lb, cm2in

# General constants
MALECOEF = 98.42
FEMALECOEF = 76.76

WAISTCOEF = 4.15
WEIGHTCOEF = 1.082

CALORIESCOEF = 13.83

def bodyfat_calc(waist, weight, waist_unit=METRIC, weight_unit=METRIC, gender=MALE, precision=2):
    """Body Fat calculator

    This formula comes from 'The Bodyfat Guide' by Ron Brown
    """
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
        factor = KILOGRAMS

    bodyfat = round(bodyfat, precision)
    fatweight = round(fatweight / factor, precision)
    lbm = round(lbm / factor, precision)
    calories = round((lbm * factor) * CALORIESCOEF, 0)

    # TODO: Code refactoring
    if gender == MALE:
        if bodyfat < 5.0:
            classification = (_(u'Essential Fat'))
        elif bodyfat > 5.0 and bodyfat < 14.0:
            classification = (_(u'Athletes'))
        elif bodyfat > 14.0 and bodyfat < 18.0:
            classification = (_(u'Fitness'))
        elif bodyfat > 18.0 and bodyfat < 25.0:
            classification = (_(u'Acceptable'))
        elif bodyfat > 25.0:
            classification = (_(u'Obese'))
    else:
        if bodyfat < 14.0:
            classification = (_(u'Essential Fat'))
        elif bodyfat > 14.0 and bodyfat < 21.0:
            classification = (_(u'Athletes'))
        elif bodyfat > 21.0 and bodyfat < 25.0:
            classification = (_(u'Fitness'))
        elif bodyfat > 25.0 and bodyfat < 32.0:
            classification = (_(u'Acceptable'))
        elif bodyfat > 32.0:
            classification = (_(u'Obese'))

    return {'bodyfat' : bodyfat, 'fatweight' : fatweight, 'lbm' : lbm,
            'calories' : calories, 'classification' : classification}
