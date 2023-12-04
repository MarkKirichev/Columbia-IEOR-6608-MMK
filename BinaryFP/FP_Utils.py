#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

import numpy as np

def fp_round(x):
    return np.array(
        [round(item) for item in x]
    )


def is_integer(x):
    for item in x:
        if not int(item) == item:
            return False
    return True


def is_feasible(x, A, b):
    for poly, n in zip(A, b):
        if poly.dot(x) > n:
            return False
    return True