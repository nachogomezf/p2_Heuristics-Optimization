import constraint
import re
import itertools as it

NUMSEATS = 32
lines = open('students.txt', 'r').read().splitlines()
students = [elem.split(',') for elem in lines]

domains =[
    list(elem) for elem in 
    list( it.product(list(range(1,NUMSEATS+1)), students) )
]
    # cartesian product (each seat possibility) x (each student)


vars = [str(i) for i in range(1,NUMSEATS+1)]
print(vars)

problem = constraint.Problem(vars, domains)
