import json
from gurobipy import read, GRB

file_root = './DatabaseMIPs/'
filename = '10teams.mps'
file_path = file_root + filename


def model_to_json(file_path, output_file_name):
    # Read the model
    model = read(file_path)

    # Extract objective function
    objective = [model.getObjective().getVar(i).getAttr("Obj") for i in range(model.numVars)]
    print(objective)

    # Extract constraints
    constraints = []
    for num_constr, constr in enumerate(model.getConstrs()):
        expr = model.getRow(constr)

        # print(f"Expression {num_constr+1}: {expr}")
        total_variables = len(objective)

        # Extracting variable indices from the expression
        variable_indices = [
            int(s[1:]) for s in str(expr).split() if s.startswith('x')
        ]

        # Creating the list with 0's and 1's
        result_list = [1 if i in variable_indices else 0 for i in range(1, total_variables + 1)]

        print(f"Coefficient {num_constr + 1}: {len(result_list)}")

        sense = constr.getAttr("Sense")
        print(sense)
        rhs = constr.getAttr("RHS")

        # Convert Gurobi sense to 'ge' or 'le'
        if sense == GRB.LESS_EQUAL:
            constraint = {"eq": result_list, "le": rhs}
        elif sense == GRB.GREATER_EQUAL:
            constraint = {"eq": result_list, "ge": rhs}
        else:
            constraint = {"eq": result_list, "le": rhs} # We'll call the EQ equations both LEQ and GEQ equations for now.
            # continue  # Skip if it's not a 'ge' or 'le' constraint
            constraints.append(constraint)
            constraint = {"eq": result_list, "ge": rhs}

        constraints.append(constraint)
        print(len(constraints))

    # Construct JSON
    data = {
        "min": objective,
        "constrs": constraints
    }

    with open(f'{output_file_name}.json', 'w') as f:
        json.dump(data, f, indent=4)

    return json.dumps(data, indent=4)


def solve_mip_model(file_path):
    # Read the model
    model = read(file_path)

    # Optimize the model
    model.optimize()

    # Check if the model has a feasible solution
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found.")
        # You can access the solution values, objective value, etc., here
        # For example, to print the objective value:
        print(f"Objective Value: {model.objVal}")
    elif model.status == GRB.INFEASIBLE:
        print("Model is infeasible.")
    elif model.status == GRB.UNBOUNDED:
        print("Model is unbounded.")
    else:
        print(f"Optimization was stopped with status {model.status}")


def gurobi_reader(file_path):

    model = read(file_path)

    constrs = model.getConstrs()

    for i in range(1, len(constrs) + 1):
        print(f"Constraint #: {i}")
        print(model.getRow(constrs[i-1]))


# Replace with the path to your file
# json_data = model_to_json(file_path)

# print(json_data)
# solve_mip_model(file_path)

model_to_json(file_path=file_path,
              output_file_name='Test_10teams')
