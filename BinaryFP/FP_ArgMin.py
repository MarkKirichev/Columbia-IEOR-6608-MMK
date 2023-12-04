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


####################
def make_delta_function(integer_solution):
    """
    Create a function to calculate the delta value for a given solution.
    The delta value is the difference between the sum of elements assigned 1 and the sum of elements assigned 0.
    """
    zero_indices = [i for i, value in enumerate(integer_solution) if value == 0]
    one_indices = [i for i, value in enumerate(integer_solution) if value == 1]
    one_count = len(one_indices)

    def delta(x):
        return x[zero_indices].sum() + one_count - x[one_indices].sum()

    return delta


def build_constraints(A, b):
    """
    Build linear constraints for optimization problem.
    """
    constraints = [optimize.LinearConstraint(A_row, -np.inf, b_val) for A_row, b_val in zip(A, b)]
    return constraints


def find_base_solution(cost, A, b, **kwargs):
    """
    Find a base solution for the linear programming problem.
    If no bounds are provided, default bounds of (0, 1) are applied to each variable.
    """
    bounds = kwargs.get('bounds', [(0, 1)] * len(cost))

    optimization_result = optimize.linprog(cost, A_ub=A, b_ub=b, bounds=bounds)
    print(optimization_result)

    if optimization_result.success:
        rounded_solution = fp_round(optimization_result.x)
        return rounded_solution, True
    else:
        return None, False


def find_arg_min(rounded_solution, constraints):
    """
    Find the argument that minimizes the delta function subject to given constraints.
    """
    hessian_matrix = np.zeros((len(rounded_solution), len(rounded_solution)))
    optimization_result = optimize.minimize(
        make_delta_function(rounded_solution),
        rounded_solution,
        method="trust-constr",
        constraints=constraints,
        bounds=optimize.Bounds(0, 1),
        hess=lambda x: hessian_matrix,
    )
    return optimization_result.x