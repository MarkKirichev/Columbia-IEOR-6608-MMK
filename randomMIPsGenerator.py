#! /usr/bin/python
# Copyright (c) 2023 Mark Kirichev

import json
import random

def generate_mip_json(num_vars, num_constr):
    # Randomly generate coefficients for the objective function
    objective = [random.randint(1, 10) for _ in range(num_vars)]

    # Generate constraints
    constraints = []
    for _ in range(num_constr):
        coeffs = [random.randint(1, 10) for _ in range(num_vars)]
        bound = random.randint(10, 100)
        if random.choice(['ge', 'le']) == 'ge':
            constraint = {"eq": coeffs, "ge": bound}
        else:
            constraint = {"eq": coeffs, "le": bound}
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
    mip_json = generate_mip_json(num_vars=num_vars,
                                 num_constr=num_constr)

    # Write the JSON data into a file
    with open(f'{output_file_name}.json', 'w') as f:
        json.dump(mip_json, f, indent=4)
