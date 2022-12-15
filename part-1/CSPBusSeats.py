from constraint import *
import os
import numpy as np
import sys

NUMSEATS = 32
with open(sys.argv[1], 'r') as f:
    lines = f.read().splitlines()
students = [elem.split(',') for elem in lines]

#If there are more students than seats available
if len(students) > NUMSEATS :
    print("ERROR: Max capacity is: {}".format(NUMSEATS))
    exit()

# VARS -> STUDENTS
# DOMAIN -> SEATS

bus = np.array(
    [
    [29, 25, 21, 17, 13, 9, 5, 1],
    [30, 26, 22, 18, 14, 10, 6, 2],
    [31, 27, 23, 19, 15, 11, 7, 3],
    [32, 28, 24, 20, 16, 12, 8, 4]
    ]
)

#function that returns the collindant elements of a matrix given the entry (a,b). Needed for troublesome students restriction
def neighbors(A, a, b):
    res = [A[i][j] for i in range(a-1, a+2) for j in range(b-1, b+2) if i > -1 and j > -1 and j < len(A[0]) and i < len(A)]
    res.remove(A[a][b])
    return res

#function that returns True if the input students are siblings, else False
def areSiblings(st1, st2):
    for st in siblings.items():
        if st == (st1,st2) or st == (st2,st1):
            return True
        else: return False

#function that returns the position of a seat in the bus in matrix entry format (i,j) (necessary to pass it to neighbors function as argument)
def seatPos(seat):
    res = []
    for elem in np.where(bus == seat):
        res.append(elem[0])
    return res


fulldomain = [i for i in range(1,33)]

domain1yr = [i for i in range(5,13)]
domain1yrR = [i for i in range(1,5)] + [i for i in range(13,17)]
domain1yrwithR = [i for i in range(1,17)]

domain2yrR = [i for i in range(17,21)]
domain2yr = [i for i in range(21,33)]

#dictionary containing the students, with the keys being their ids'
studentsDict = {st[0] : st for st in students}

students1yr = [st[0] for st in students if st[1] == '1']
students2yr = [st[0] for st in students if st[1] == '2']

oldBrothers = []
youngBrothers = []
for index, st in enumerate(students):
    if st[1] == '2' and st[4] in students1yr:
        students[index][1] = '1'
        oldBrothers.append(st[0])
        youngBrothers.append(st[4])
        #if the siblings are from different years, change the second year to be first year too internally as both will go in the front
        # As we are losing the info about who is older, we save it into the aux list oldBrothers in order to know later who to place in the aisle

allstudents = [st[0] for st in students]
    
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
#adding 1st year normal and troublesome to the domain: "any seat in the front"
problem.addVariables(students1XX + students1CX, domain1yrwithR)
#adding 1st year normal and troublesome to the domain: "any seat in the back"
problem.addVariables(students2XX + students2CX, domain2yrR + domain2yr)
#adding 1st year handicapped (either normal or troublesome) to their special seats in the front
problem.addVariables(students1XR + students1CR, domain1yrR)
#adding 2st year handicapped (either normal or troublesome) to their special seats in the back
problem.addVariables(students2XR + students2CR, domain2yrR)

problem.addConstraint(AllDifferentConstraint())

# Dictionary of siblings, with the key being the younger brother always and the value the older
siblings = {}

for st in students: 
    # If brothers are truly from the same year, add one pair of siblings to the dict 
    # (arbitrarily choose the pair with the key being associated to student with lower id)
    if st[0] not in oldBrothers and st[0] not in youngBrothers and st[0] < st[4]:
        siblings[st[0]] = st[4]
    else:
    # Else, if brothers were from different years, assign the younger as key so that we can identify later who to assign the window and aisle
        if st[0] in youngBrothers: 
            siblings[st[0]] = st[4]

#REDUCED MOBILITY RESTRICTION

def redMob(seat1, seat2):
    if seat1 % 2 == 1: # odd seats
        if seat2 != seat1 + 1: return True
    else:                                # even seats
        if seat1 != seat2 + 1: return True

for st1 in studentsXR+studentsCR: # iterate through the disabled students
    for st2 in allstudents: # iterate through all students so that they cannot seat next to the reduced mobility student
        if st1 != st2:
            problem.addConstraint(
                                redMob,
                                (st1, st2)
                                ) #next seat to reduced mobility must be free

# SIBLINGS RESTRICTION

def sibs(seat1, seat2):
    if seat1 % 2 == 1: # odd seats
        if seat2 == seat1 + 1: return True
    else:                                # even seats
        if seat1 == seat2 + 1: return True

for sib in siblings.items(): 
#   We need to check that none of the siblings are handicapped, since if one or both of them are, they cannot be seated together
    if studentsDict[sib[0]][3] != 'R' and studentsDict[sib[1]][3] != 'R':
        if sib[0] in youngBrothers:
            problem.addConstraint(
                lambda young, old: (young % 4 == 1 and old == young+1) or (young % 4 == 0 and young == old +1),
                # mod 4 == 1 means the seat is aligned with driver's window, therefore the old sibling's seat will be 1 unit bigger for it to be aisle
                # mod 4 == 0 means the other window, therefore the old sibling's seat will be 1 unit lesser for it to be aisle
                (sib[0], sib[1])
            )
        else:
            problem.addConstraint(
                sibs,
                (sib[0], sib[1])
            )

#TROUBLESOME STUDENTS RESTRICTION

for stC in studentsCR + studentsCX: #troublesome students
    for st2 in studentsCR + studentsCX + studentsXR: #troublesome and disabled students
        if stC != st2  and not areSiblings(stC, st2):
            problem.addConstraint(
            lambda seat1, seat2: seat2 not in neighbors(bus, seatPos(seat1)[0], seatPos(seat1)[1])
            ,(stC, st2)
            )

sol = problem.getSolution()
sols = problem.getSolutions()

#function that sorts a dictionary by value
def sorted_dict(sol): return dict(sorted(sol.items(), key=lambda item: item[1]))

#function to format the solution dictionary
def formatSol(sol): return sorted_dict({str(st + studentsDict[st][2] + studentsDict[st][3]) : sol[st] for st in sol})

output = open(os.path.splitext(sys.argv[1])[0] + '.output', 'w')
output.write("Number of solutions: {}\n".format(len(sols)))

#print at least the first ten solutions (if they exist)
for i in range(10):
    if i < len(sols) and sols != []: 
        output.write(str(formatSol(sols[i])) + '\n')