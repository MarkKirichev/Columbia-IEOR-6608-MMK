import json
import random

def generate_mip_json(num_vars=2025, num_constr=230):
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

# Generate the JSON data
mip_json = generate_mip_json()

# Print the JSON data
with open('Test_random2025.json', 'w') as f:
    json.dump(mip_json, f, indent=4)
