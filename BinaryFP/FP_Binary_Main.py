#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import logging

from .FP_ArgMin import find_base_solution, build_constraints, find_arg_min
from .FP_Utils import is_integer, is_feasible, fp_round
from .FP_FlipSol import flip_solution


def need_update(x, rx):
    return any(round(i) != j for i, j in zip(x, rx))

def update_round(sol, int_sol):
    return fp_round(sol) if need_update(sol, int_sol) else flip_solution(sol, int_sol)

def feasibility_pump(c, A, b, log):

    if log:
        logging.basicConfig(level=logging.INFO, format='%(message)s')

    # Define the bounds here
    # Put in 0 and 1 for a binary MIP
    bounds = {
        'min': 0,
        'max': 1,
    }

    rx, stat = find_base_solution(c, A, b, bounds=[(bounds['min'],
                                                    bounds['max'])])
    logging.info('solved LP relaxation')

    print('solved LP relaxation')

    if not stat:
        logging.info('LP relaxation has no solution - done')
        print('LP relaxation has no solution - done')
        return None, False

    constr = build_constraints(A, b)

    if is_feasible(rx, A, b):
        logging.info('rounded solution is feasible - done')
        print('rounded solution is feasible - done')
        return rx, True

    for _ in range(len(c) * 10):

        tmp = find_arg_min(rx, constr)
        logging.info('solved fp delta')
        print('solved fp delta')
        if is_integer(tmp):
            logging.info('fp delta solution is integer - done')
            print('fp delta solution is integer - done')
            out = tmp, True
            break

        rx = update_round(tmp, rx)

        if is_feasible(rx, A, b):
            logging.info('rounded solution is feasible - done')
            print('rounded solution is feasible - done')
            out = rx, True
            break

    else:
        logging.info('no feasible solution found')
        print('no feasible solution found')
        out = None, False

    return out
