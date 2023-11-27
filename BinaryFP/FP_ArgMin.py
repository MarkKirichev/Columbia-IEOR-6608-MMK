#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

import numpy as np
from scipy import optimize

from .FP_Utils import fp_round


def fp_make_delta(int_sol):
    zeros = [i for i, j in enumerate(int_sol) if j == 0]
    ones = [i for i, j in enumerate(int_sol) if j == 1]
    amount = len(ones)

    def __out__(x):
        return x[zeros].sum() + amount - x[ones].sum()

    return __out__


def build_constr(A, b):
    out = [optimize.LinearConstraint(poly, -np.inf, n) for poly, n in zip(A, b)]
    return out


def base_sol(c, A, b, **kwargs):

    if not 'bounds' in kwargs.keys():
        bounds = [(0, 1)] * len(c)
    else:
        bounds = kwargs['bounds'] * len(c)

    print(type(A))
    res = optimize.linprog(c, A_ub=A, b_ub=b, bounds=bounds)
    print(res)

    if res.success:
        x = fp_round(res.x)
        out = x, True
    else:
        out = None, False
    return out


def arg_min(rx, constr):

    hess = np.zeros((len(rx), len(rx)))
    tmp = optimize.minimize(
        fp_make_delta(rx),
        rx,
        method="trust-constr",
        constraints=constr,
        bounds=optimize.Bounds(0, 1),
        hess=lambda x: hess,
    )
    return tmp.x
