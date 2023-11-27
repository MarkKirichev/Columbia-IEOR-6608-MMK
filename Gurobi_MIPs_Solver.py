import json
from gurobipy import read, GRB

file_root = './DatabaseMIPs/'
filename = '10teams.mps'
file_path = file_root + filename


def model_to_json(file_path):
    # Read the model
    model = read(file_path)

    # Extract objective function
    objective = [model.getObjective().getVar(i).getAttr("Obj") for i in range(model.numVars)]
    print(objective)

    # Extract constraints
    constraints = []
    for constr in model.getConstrs():
        expr = model.getRow(constr)
        coeffs = [expr.getCoeff(i) for i in range(expr.size())]
        sense = constr.getAttr("Sense")
        rhs = constr.getAttr("RHS")

        # Convert Gurobi sense to 'ge' or 'le'
        if sense == GRB.LESS_EQUAL:
            constraint = {"eq": coeffs, "le": rhs}
        elif sense == GRB.GREATER_EQUAL:
            constraint = {"eq": coeffs, "ge": rhs}
        else:
            continue  # Skip if it's not a 'ge' or 'le' constraint

        constraints.append(constraint)

    # Construct JSON
    data = {
        "min": objective,
        "constrs": constraints
    }

    # with open('Test_10teams.json', 'w') as f:
    #     json.dump(data, f, indent=4)

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


# Replace with the path to your file
json_data = model_to_json(file_path)
print(json_data)

solve_mip_model(file_path)
