#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import json
import random

def generate_feasible_mip_json(num_vars, num_constr,
                               obj_min=1, obj_max=10,
                               coeff_min=0, coeff_max=1): # the coeffs. are 0 and 1 for binary constraints
    # Generate a random feasible solution
    feasible_solution = [random.choice([0, 1]) for _ in range(num_vars)]

    # Generate objective function
    objective = [random.randint(obj_min, obj_max) for _ in range(num_vars)]

    # Generate constraints that are satisfied by the feasible solution
    constraints = []
    for _ in range(num_constr):
        coeffs = [random.randint(coeff_min, coeff_max) for _ in range(num_vars)]  # Coefficients are either 0 or 1
        # Calculate the constraint bound to ensure it's feasible
        bound = sum(
            [coeff * var for coeff, var in zip(coeffs, feasible_solution)]
        )
        if random.choice(['ge', 'le']) == 'ge':
            constraint = {
                "eq": coeffs,
                "ge": bound
            }
        else:
            # For 'le', increase the bound to ensure feasibility
            constraint = {
                "eq": coeffs,
                "le": bound + random.randint(0, 5)
            }
        constraints.append(constraint)

    # Construct JSON data
    mip_data = {
        "min": objective,
        "constrs": constraints
    }

    return mip_data


if __name__ == '__main__':
    output_file_name = input()

    # Set the number of variables and constraints
    num_vars = 2025
    num_constr = 230

    # Generate the JSON data
    mip_json = generate_feasible_mip_json(num_vars=num_vars,
                                          num_constr=num_constr)

    # Write the JSON data into a file
    with open(f'{output_file_name}.json', 'w') as f:
        json.dump(mip_json, f, indent=4)

    # Optional: Print out the randomly created JSON file
    print(json.dumps(mip_json, indent=4))
