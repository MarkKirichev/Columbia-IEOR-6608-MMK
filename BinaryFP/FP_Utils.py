#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

import numpy as np

def fp_round(x):
    tmp = map(round, x)
    return np.array(list(tmp))


def is_integer(x):
    for i in x:
        if not int(i) == i:
            return False
    return True


def is_feasible(x, A, b):
    for poly, n in zip(A, b):
        if poly.dot(x) > n:
            return False
    return True