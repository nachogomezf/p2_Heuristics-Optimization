import constraint
import re
import itertools as it

NUMSEATS = 32
lines = open('students.txt', 'r').read().splitlines()
students = [elem.split(',') for elem in lines]

domains =[
    [a] + b for a in range(1, NUMSEATS+1) for b in students
]
    # cartesian product (each seat possibility) x (each student)


vars = [str(i) for i in range(1,NUMSEATS+1)]
print(vars)
print(domains[0:32])

problem = constraint.Problem()
problem.addVariables('1', domains[0:31])
for i, elem in enumerate(vars):
    problem.addVariables(elem, str(domains[(i-1)*32:i*32]))


