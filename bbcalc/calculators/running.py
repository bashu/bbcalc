# -*- coding: utf-8 -*-

from bbcalc.utils import IMPERIAL, METRIC

from bbcalc.utils.unitconvertor import km2mi, kg2lb


def running_calc(weight, distance, weight_unit=METRIC, distance_unit=METRIC, precision=2):
    """Calorie Burning: Running calculator"""
    if weight_unit != IMPERIAL:
        weight = kg2lb(float(weight))
    if distance_unit != IMPERIAL:
        distance = km2mi(float(distance))

    # Formulae: calories burned = (distance * weight) * 0.653
    difference = round(((distance * weight) * 0.653), precision)

    return difference
