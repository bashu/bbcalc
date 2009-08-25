# -*- coding: utf-8 -*-

from gettext import gettext as _

from bbcalc.utils import IMPERIAL, METRIC

from bbcalc.utils.unitconvertor import lb2kg, in2cm


def bmi_calc(height, weight, height_unit=METRIC, weight_unit=METRIC, precision=1):
    """Body Mass Index (for adults) calculator"""
    if height_unit == IMPERIAL:
        height = in2cm(float(height))
    if weight_unit == IMPERIAL:
        weight = lb2kg(float(weight))

    # Convert height from centimeters to meters
    height = height / 100
    # Formulae: bmi = kg / m^2
    bmi = round((weight / (height ** 2)), precision)

    # TODO: Code refactoring
    if bmi < 18.5:
        status = (_(u'Underweight'))
    elif bmi > 18.5 and bmi < 24.9:
        status = (_(u'Normal'))
    elif bmi > 24.9 and bmi < 30.0:
        status = (_(u'Overweight '))
    elif bmi > 30.0:
        status = (_(u'Obese'))
    else:
        status = unicode()

    return {'bmi' : bmi, 'status' : status}
