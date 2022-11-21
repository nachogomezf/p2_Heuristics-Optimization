import ast

with open('students.prob') as f:
    data = f.read()

# reconstructing the data as a dictionary
initial_q = ast.literal_eval(data)

# We will search by iteratively taking each student as initial node and performing A*. Then we'll take the cheaper option.

print(initial_q )