# -*- coding: utf-8 -*-

# General constants
WRISTCOEF = [6.5, 0.85, 0.70, 0.53, 0.37, 0.36, 0.34, 0.29]


def ideal_body_calc(wrist, precision=2):
    """Ideal Body Measurements (for men) calculator"""
    array = [wrist]
    array.append(array[0] * WRISTCOEF[0])
    for idx in xrange(1, 8):
        array.append(array[1] * WRISTCOEF[idx])

    for idx in xrange(0, 9):
        array[idx] = round((array[idx] + 0.0001) * 100, precision)
        array[idx] = round(array[idx] / 100.0, precision)
    return array

