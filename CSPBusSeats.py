from constraint import *
import os
import numpy as np
import sys

NUMSEATS = 32
lines = open(sys.argv[1], 'r').read().splitlines()
students = [elem.split(',') for elem in lines]

if len(students) > NUMSEATS :
    print("ERROR: Max capacity is: {}".format(NUMSEATS))
    exit()

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


def removeFrom(l: list, elems: list):
    return [e for e in l if e not in elems]

def neighbors(A, a, b):
    res = [A[i][j] for i in range(a-1, a+2) for j in range(b-1, b+2) if i > -1 and j > -1 and j < len(A[0]) and i < len(A)]
    res.remove(A[a][b])
    return res

def studentAt(list, val):
    for index, st in enumerate(list):
        if st[0] == val:
            return index

def areSiblings(st1, st2):
    for st in siblings.items():
        if st == (st1,st2) or st == (st2,st1):
            return True
        else: return False

def seatPos(seat):
    res = []
    for elem in np.where(bus == seat):
        res.append(elem[0])
    return res

fulldomain = [i for i in range(1,33)]

domain1yr = [i for i in range(5,13)]
domain1yrwithC = [i for i in range(1,17)]

domain2yrC = [i for i in range(17,21)]
domain2yr = [i for i in range(21,33)]
domain1yrC = [i for i in range(1,5)] + [i for i in range(13,17)]



studentsDict = {st[0] : st for st in students}

students1yr = [st[0] for st in students if st[1] == '1']
students2yr = [st[0] for st in students if st[1] == '2']

for index, st in enumerate(students):
    if st[1] == '2' and st[4] in students1yr:
        students[index][1] = '1'
        #change the second year to student to be first year internally if they are siblings from different years

allstudents = [st[0] for st in students]

'''siblings12R = [[st[0] , st[4]] for st in students if st[1] == '1' and st[4] in students2yr and (st[3] == 'R' or studentsDict[st[4]][3] == 'R')]
siblings12yr = [[st[0], st[4]] for st in students if st[1] == '1' and st[4] in students2yr and st[3] != 'R' and studentsDict[st[4]][3] != 'R']

siblings12yr = sum(siblings12yr, [])
siblings12R = sum(siblings12R, [])
studentsNoSiblings = [st for st in students if st[0] not in siblings12yr and st[0] not in siblings12R]

students1yr = removeFrom(students1yr, siblings12yr)
students1yr = removeFrom(students1yr, siblings12R)

students2yr = removeFrom(students2yr, siblings12R)
students2yr = removeFrom(students2yr, siblings12yr)
'''



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



problem = Problem()
# problem.addVariables(siblings12yr, domain1yrwithC)
problem.addVariables(students1XX + students1CX, domain1yrwithC)
problem.addVariables(students2XX + students2CX, domain2yrC + domain2yr)
problem.addVariables(students1XR + students1CR, domain1yrC)
problem.addVariables(students2XR + students2CR, domain2yrC)

problem.addConstraint(AllDifferentConstraint())

# Dictionary of siblings, with the key being the younger brother always
siblings = {st[0] : st[4] for st in students if st[4] > '0' and st[0] <= students[studentAt(students, st[4])][0]}

# SIBLINGS RESTRICTION
for sib in siblings.items(): 
    if studentsDict[sib[0]][3] != 'R' and studentsDict[sib[1]][3] != 'R':
        problem.addConstraint(
            lambda young, old: (young % 4 == 1 and old == young+1) or (young % 4 == 0 and young == old +1),
            (sib[0], sib[1])
        )

#REDUCED MOBILITY RESTRICTION

def redMob(seat1, seat2):
    if seat1 % 4 == 1 or seat1 % 4 == 3:
        if seat2 != seat1 + 1: return True
    else:
        if seat1 != seat2 + 1: return True

for st1 in studentsXR+studentsCR:
    for st2 in allstudents:
        if st1 != st2:
            problem.addConstraint(
                                redMob,
                                (st1, st2)
                                ) #next seat to reduced mobility must be free


#TROUBLESOME STUDENTS RESTRICTION



for stC in studentsCR + studentsCX: #troublesome students
    for st2 in studentsCR + studentsCX + studentsXR: #troublesome and disabled students
        if stC != st2  and not areSiblings(stC, st2):
            problem.addConstraint(
            lambda seat1, seat2: seat2 not in neighbors(bus, seatPos(seat1)[0], seatPos(seat1)[1])
            ,(stC, st2)
            )

#What happens if one is brother is troubled and the other is disabled??? Se sientan juntos con esta version... not sure si esta bien



sol = problem.getSolution()
sols = problem.getSolutions()

def sorted_dict(sol): return { sorted(sol.items(), key=lambda item: item[1]) } 
    
def formatSol(sol): return sorted_dict({str(st + studentsDict[st][2] + studentsDict[st][3]) : sol[st] for st in sol})

output = open(os.path.splitext(sys.argv[1])[0] + '.output', 'w')
output.write("Number of solutions: {}\n".format(len(sols)))

for i in range(5):
    if i <= len(sols): output.write(str(formatSol(sols[i])) + '\n')