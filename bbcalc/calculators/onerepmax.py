# -*- coding: utf-8 -*-

# General constants
REPCOEF = [0, 1, 0.955, 0.917, 0.885, 0.857, 0.832, 0.809,
           0.788, 0.769, 0.752, 0.736, 0.721, 0.706, 0.692, 0.678]

def onerep_max_calc(weight, reps, precision=2):
    """One-Rep Maximum calculator

    This formula comes from 'A Practical Approach to Strength Training' by
    Matt Brzycki
    """
    return round(weight / REPCOEF[reps], precision)
