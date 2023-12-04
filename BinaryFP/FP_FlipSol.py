#! /usr/bin/python

# Copyright (c) 2023 Mark Kirichev

from secrets import randbelow


def fp_error(original, rounded):
    """
    Calculate the error between the original and rounded solutions.
    Returns a dictionary mapping the error to the index in the solution.
    """
    error_to_index = {
        abs(orig - round_val): idx for idx, (orig, round_val) in enumerate(
            zip(original, rounded)
        )
    }
    return error_to_index

def flip_solution(original, rounded):
    """
    Flip the solution based on the calculated error.
    Randomly selects a starting point and flips the bits in the rounded solution from that point onwards.
    """
    error_dict = fp_error(original=original,
                          rounded=rounded)
    sorted_errors = sorted(error_dict.keys())

    end = len(original)
    start = randbelow(end - 1) + 1
    for error in sorted_errors[start:end]:
        index = error_dict[error]
        rounded[index] = (rounded[index] + 1) % 2

    return rounded