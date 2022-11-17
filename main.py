from constraint import *
import re
import numpy as np

NUMSEATS = 32
lines = open('students2.txt', 'r').read().splitlines()
students = [elem.split(',') for elem in lines]

# VARS -> STUDENTS
# DOMAIN -> SEATS

frontseats = np.array(
    [
    [29,25,21,17],
    [30, 26, 22, 18],
    [31, 27, 23, 19],
    [32, 28, 24, 20]
    ]
)
backseats = np.array(
    [
        [13, 9, 5, 1],
        [14, 10, 6, 2],
        [15, 11, 7, 3],
        [16, 12, 8, 4]
    ]
)
reducedmob1 = np.array(
    [
    [13, 1],
    [14, 2],
    [15, 3],
    [16, 4]
]
)

reducedmob2 = (np.array ([17, 18, 19, 20])).T
def neighbors(A, a, b):
    return [A[i][j] for i in range(a-1, a+2) for j in range(b-1, b+2) if i > -1 and j > -1 and j < len(A[0]) and i < len(A)]

seats = np.hstack((frontseats, backseats))

domain1yr = [i for i in range(5,13)]
domain1yrC = [i for i in range(1,17)]
domain2yr = [i for i in range(21,33)]
domainC = [i for i in range(1,5)] + [i for i in range(13,17)] + [i for i in range(17,21)]



allstudents = [st[0] for st in students]
students1yr = [st[0] for st in students if st[1] == '1']
students2yr = [st[0] for st in students if st[1] == '2']
studentsCX = [st[0] for st in students if st[2] == 'C']
studentsCR = [st[0] for st in students if st[2] == 'X']
studentsXR = [st[0] for st in students if st[2] == 'X' and st[3] == 'R']
studentsXX =  [st[0] for st in students if st[2] == 'X' and st[3] == 'R']

print("First year domain:",  domain1yr, "Second year domain:", domain2yr)
print("First year students: ", students1yr, "Second year students: ", students2yr)


problem = Problem()
problem.addVariables(students1yr, domain1yr)
problem.addVariables(students2yr, domain2yr)
problem.addConstraint(AllDifferentConstraint())
print(problem.getSolution())
'''
for i, elem in enumerate(vars):
    problem.addVariables(elem, str(domains[(i-1)*32:i*32]))'''


