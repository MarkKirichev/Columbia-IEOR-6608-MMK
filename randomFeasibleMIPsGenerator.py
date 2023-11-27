import json
import random

def generate_feasible_mip_json(num_vars=260, num_constr=80):
    # Generate a random feasible solution
    feasible_solution = [random.choice([0, 1]) for _ in range(num_vars)]

    # Generate objective function
    objective = [random.randint(1, 10) for _ in range(num_vars)]

    # Generate constraints that are satisfied by the feasible solution
    constraints = []
    for _ in range(num_constr):
        coeffs = [random.randint(0, 1) for _ in range(num_vars)]  # Coefficients are either 0 or 1
        # Calculate the constraint bound to ensure it's feasible
        bound = sum([coeff * var for coeff, var in zip(coeffs, feasible_solution)])
        if random.choice(['ge', 'le']) == 'ge':
            constraint = {"eq": coeffs, "ge": bound}
        else:
            # For 'le', increase the bound to ensure feasibility
            constraint = {"eq": coeffs, "le": bound + random.randint(0, 5)}
        constraints.append(constraint)

    # Construct JSON data
    mip_data = {
        "min": objective,
        "constrs": constraints
    }

    return mip_data

# Generate the JSON data
mip_json = generate_feasible_mip_json()

# Print the JSON data
print(json.dumps(mip_json, indent=4))

with open('Test_random260_feasible.json', 'w') as f:
    json.dump(mip_json, f, indent=4)