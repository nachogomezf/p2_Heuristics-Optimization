from constraint import *
import re
import numpy as np

NUMSEATS = 32
lines = open('students2.txt', 'r').read().splitlines()
students = [elem.split(',') for elem in lines]

# VARS -> STUDENTS
# DOMAIN -> SEATS

backseats = np.array(
    [
    [29,25,21,17],
    [30, 26, 22, 18],
    [31, 27, 23, 19],
    [32, 28, 24, 20]
    ]
)
frontseats = np.array(
    [
        [13, 9, 5, 1],
        [14, 10, 6, 2],
        [15, 11, 7, 3],
        [16, 12, 8, 4]
    ]
)
reducedmob1 = (np.array ([[1, 2, 3, 4]])).T
reducedmob2 = (np.array ([[13, 14, 15, 16]])).T
reducedmob3 = (np.array ([[17, 18, 19, 20]])).T
bus = np.hstack(( backseats, frontseats))
mirrorbus = np.ones((4,8), int)
for j in range (1,8):
    mirrorbus[:, j-1] = bus[:,-j]
mirrorbus[:, 7] = bus[:, 0]

print(mirrorbus)
def neighbors(A, a, b):
    return [A[i][j] for i in range(a-1, a+2) for j in range(b-1, b+2) if i > -1 and j > -1 and j < len(A[0]) and i < len(A)]
 
seats = np.hstack((frontseats, backseats))

domain1yr = [i for i in range(5,13)]
domain1yrwithC = [i for i in range(1,17)]

domain2yrC = [i for i in range(17,21)]
domain2yr = [i for i in range(21,33)]
domain1yrC = [i for i in range(1,5)] + [i for i in range(13,17)]



allstudents = [st[0] for st in students]

students1yr = [st[0] for st in students if st[1] == '1']
students2yr = [st[0] for st in students if st[1] == '2']

studentsCX = [st[0] for st in students if st[2] == 'C' and st[3] == 'X']
studentsCR = [st[0] for st in students if st[2] == 'C' and st[3] == 'R']
studentsXR = [st[0] for st in students if st[2] == 'X' and st[3] == 'R']
studentsXX =  [st[0] for st in students if st[2] == 'X' and st[3] == 'X']

students1XX = [st[0] for st in students if st[1] == '1' and st[2] == 'X' and st[3] == 'X']
students1CX = [st[0] for st in students if st[1] == '1' and st[2] == 'C' and st[3] == 'X']
students1XR = [st[0] for st in students if st[1] == '1' and st[2] == 'X' and st[3] == 'R']
students1CR = [st[0] for st in students if st[1] == '1' and st[2] == 'C' and st[3] == 'R']

students2XX = [st[0] for st in students if st[1] == '2' and st[2] == 'X' and st[3] == 'X']
students2CX = [st[0] for st in students if st[1] == '2' and st[2] == 'C' and st[3] == 'X']
students2XR = [st[0] for st in students if st[1] == '2' and st[2] == 'X' and st[3] == 'R']
students2CR = [st[0] for st in students if st[1] == '2' and st[2] == 'C' and st[3] == 'R']

print("First year domain:",  domain1yr, "Second year domain:", domain2yr)
print("First year students: ", students1yr, "Second year students: ", students2yr)


problem = Problem()
problem.addVariables(students1XX + students1CX, domain1yr)
problem.addVariables(students2XX + students2CX, domain2yr)
problem.addVariables(students1XR + students1CR, domain1yrC)
problem.addVariables(students2XR + students2CR, domain2yrC)



problem.addConstraint(AllDifferentConstraint())

for st1 in studentsXR+studentsCR:
    for st2 in studentsXR+studentsCR:
        if st1 != st2:
            problem.addConstraint(
                                lambda seat1, seat2: seat1 != seat2+1 and seat1 != seat2-1,
                                (st1, st2)
                                 ) #next seat to reduced mobility must be free

# TODO
# define seatToPos function: converts a given seat into the corresponding entry of the matrix bus (ormirrorbus)

'''for stC in studentsCR + studentsCX: #troublesome students
    for st2 in studentsCR + studentsCX + studentsXR: #troublesome and disabled students
        if stC != st2:
            problem.addConstraint(
                lambda seat1, seat2:
                    for elem in neighbors(mirrorbus, seatToPos):
                        elem
            )'''

print(problem.getSolution())

'''
for i, elem in enumerate(vars):
    problem.addVariables(elem, str(domains[(i-1)*32:i*32]))'''


