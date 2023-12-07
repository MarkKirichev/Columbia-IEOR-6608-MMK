#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import numpy as np
from scipy import optimize

from .FP_Utils import fp_round

def make_delta_function(integer_solution):
    # Create a function to calculate the delta value for a given solution.
    # The delta value is the difference between the sum of elements assigned 1 and the sum of elements assigned 0.

    zero_indices = [i for i, value in enumerate(integer_solution) if value == 0]
    one_indices = [i for i, value in enumerate(integer_solution) if value == 1]
    one_count = len(one_indices)

    def delta(x):
        return x[zero_indices].sum() + one_count - x[one_indices].sum()

    return delta


def build_constraints(A, b):
    # Build linear constraints for optimization problem.

    constraints = [optimize.LinearConstraint(A_row, -np.inf, b_val) for A_row, b_val in zip(A, b)]
    return constraints


def find_base_solution(cost, A, b, **kwargs):
    # Find a base solution for the linear programming problem.
    # If no bounds are provided, default bounds of (0, 1) are applied to each variable.

    bounds = kwargs.get('bounds', [(0, 1)] * len(cost))

    optimization_result = optimize.linprog(cost, A_ub=A, b_ub=b, bounds=bounds)
    print(optimization_result)

    if optimization_result.success:
        rounded_solution = fp_round(optimization_result.x)
        return rounded_solution, True
    else:
        return None, False


def find_arg_min(rounded_solution, constraints):
    # Find the argument that minimizes the delta function subject to given constraints.

    hessian_matrix = np.zeros(
        (len(rounded_solution),
         len(rounded_solution))
    )
    optimization_result = optimize.minimize(
        make_delta_function(rounded_solution),
        rounded_solution,
        method="trust-constr",
        constraints=constraints,
        bounds=optimize.Bounds(0, 1),
        hess=lambda x: hessian_matrix,
    )
    return optimization_result.x
