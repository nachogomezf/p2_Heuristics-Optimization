import ast
import time
import sys
import os

class Node:
    def __init__(self, students: list =[], remaining: list =[]):
        self.state = students
        self.remaining = remaining
        self.cost = 0
        if students:
            # if there was at least a student in the queue, check if it was reduced mobility
            if students[0].rm:
                self.cost = 3
            else:
                self.cost = 1
        self.heuristic = len(remaining) if sys.argv[2] == '1' else 0
        prev = None
        tr_seats = []
        for i in students:
            if i.tr:
                tr_seats.append(i.seat)
            for elem in tr_seats:
                if i.seat > elem:
                    if i.tr: self.cost += 3
                    else: self.cost += 1
            if prev:
                if not prev.rm:
                    if prev.tr:
                        if i.rm: self.cost += 6
                        else: self.cost += 2
                    # not trouble
                    else:
                        if i.rm: self.cost += 3
                        else: self.cost += 1
                else:
                    if i.tr:
                        self.cost += 3
            prev = i
        self.parent = None
        if self.parent:
            self.cost += self.parent.cost
        self.totalcost = self.cost + self.heuristic

class Student:
    def __init__(self, id, seat, tr, rm) -> None:
        self.id = id
        self.seat = seat
        self.tr = True if tr == 'C' else False
        self.rm = True if rm == 'R' else False

def getStudents(students):
    res = []
    for i, j in students.items():
        res.append(Student(i[:-2], j, i[-2], i[-1]))
    return res

def children(node):
    res = []
    # Mete los operadores y restricciones aqui
    
    for i in node.remaining:
        if node.state:
            if node.state[-1].rm and i.rm:
                # if prev and current are R, do not generate the child since we cannot have two consecutive disabled students
                continue
        mylist = node.remaining.copy()
        mylist.remove(i)
        res.append(Node(node.state + [i], mylist))
    return res


def astar(students):
    openset = set()
    closedset = set()
    current = Node([], students)
    openset.add(current)

    while openset:
        current = min(openset-closedset, key=lambda i : i.totalcost)
        if current.state and (not current.remaining) and current.state[-1] != 'R': return openset, closedset, current
        openset.remove(current)
        closedset.add(current)
        for node in children(current): 
            openset.add(node)
            node.parent = current
            

if __name__ == '__main__':
    start = time.time()
    '''with open(sys.argv[1], 'r') as f:
        data = f.read()'''
    with open('students.prob', 'r') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    students = ast.literal_eval(data)
    open, closed, result = astar(getStudents(students))
    end = time.time()

    res = {}
    for s in result.state:
        res[s.id + ('C' if s.tr else 'X') + ('R' if s.rm else 'X')] = s.seat

    fname = "{}-{}".format(os.path.splitext(sys.argv[1])[0], sys.argv[2]) 
    with open(fname + '.output', 'w') as output:
        output.write("INITIAL:\t{} \nFINAL:\t{}".format(data, res))

    with open(fname + '.stat', 'w') as stat:
        stat.write("Total time: {}\nPlan cost: {}\nExpanded nodes: {}\nPlan length: {}", end-start, result.cost, len(open), len(closed))
