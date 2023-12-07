#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import numpy as np

def fp_round(x):
    return np.array(
        [round(item) for item in x]
    )

def is_integer(x):
    return all(
        int(item) == item for item in x
    )

def is_feasible(x, A, b):
    return all(poly.dot(x) <= n for poly, n in zip(A, b))
