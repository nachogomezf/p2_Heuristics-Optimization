import ast
import time
import sys
import os

class Node:
    def __init__(self, students: list =[], remaining: list =[]):
        # current state of the search is the students that have been already assigned a place in the queue (boarded)
        self.state = students
        # to keep track of costs and heuristics we also keep a list with the students who haven't been assigned yet
        self.remaining = remaining
        # initialize the cost for the current state
        self.cost = 0
        if students:
            # if there is at least one student in the queue, check if it is a reduced mobility
            if students[0].rm:
                self.cost = 3
            else:
                self.cost = 1
        # here we define two heuristics: first, the one in which we disregard both the reduced mobility and troublesome conditions and second, every entry has cost 0 (dijkstra)
        # note that both heuristics are admissible they will never overestimate the total cost
        self.heuristic = len(remaining) if sys.argv[2] == '1' else 0
        prev = None
        tr_seats = []
        for i in students:
            # keep track of the troublesome students that have already boarded the bus so that we can check other restrictions from the problem statement
            if i.tr:
                tr_seats.append(i.seat)
            # compare the current student's seat number to check if any troublesome student with a lower seat number has already boarded
            for elem in tr_seats:
                if i.seat > elem:
                    if i.tr: self.cost += 3
                    else: self.cost += 1
            # due to the reduced mobility and troublesome restrictions, we need to check the student that went in before the current one, we use prev for that
            if prev:
                # if it was not reduced mobility
                if not prev.rm:
                    # troublesome
                    if prev.tr:
                        if i.rm: self.cost += 6
                        else: self.cost += 2
                    # not troublesome
                    else:
                        if i.rm: self.cost += 3
                        else: self.cost += 1
                # if it was reduced mobility and our current student has no restrictions, then the time for both of them is the time of the first one (3), so we don't add any more time
                # whereas, if our current student is troublesome, it will double them both time, so we add 3 to the total cost (time)
                else:
                    if i.tr:
                        self.cost += 3
            prev = i
        self.parent = None
        # ELIMINATE?
        if self.parent:
            self.cost += self.parent.cost
        self.totalcost = self.cost + self.heuristic

class Student:
    def __init__(self, id, seat, tr, rm) -> None:
        # define the attributes for the student class, that is, the information that defines each student
        self.id = id
        self.seat = seat
        self.tr = True if tr == 'C' else False
        self.rm = True if rm == 'R' else False

# function to organize the list of students from raw data into a list made of our Student structures
def getStudents(students):
    res = []
    for i, j in students.items():
        # for the id, we get everything but the last two letters of the student's info
        # seat number is given (j)
        # rm and tr are extracted from the two last characters in i, getting either R or X, or C or X, respectively
        res.append(Student(i[:-2], j, i[-2], i[-1]))
    return res

def children(node):
    res = []
    # here go the operators defined by the restrictions of the problem    
    # iterate through the remaining students and, if possible, generate a node with each of them (adding one student to the state list and removing it from the remaining list)
    for i in node.remaining:
        if node.state:
            if node.state[-1].rm and i.rm:
                # if prev and current are rm, do not generate the child since we cannot have two consecutive disabled students
                continue
        mylist = node.remaining.copy()
        mylist.remove(i)
        res.append(Node(node.state + [i], mylist))
    return res


def astar(students):
    openset = set()
    closedset = set()
    # initial state, with the empty state and the remaining list with the full list of students
    current = Node([], students)
    # add it to the open set so we can start to expand it
    openset.add(current)
    # only stop whenever there are not more nodes to expand (no solution) or an optimal solution has been found (later in the code)
    while openset:
        # select the node with the minimum total cost (cost + heuristic) to expand
        current = min(openset-closedset, key=lambda i : i.totalcost)
        # if the remaining list of students is empty it means that we have reached the goal state. Here we also check that no reduced mobility student has been added last (without help to get in)
        if current.state and (not current.remaining) and not current.state[-1].rm: 
            print("last")
            return openset, closedset, current
        # once the node has been expanded, we take it out of the open set and incude it into the closed set, so it cannot be expanded again
        openset.remove(current)
        closedset.add(current)
        # expand the selected node
        for node in children(current): 
            openset.add(node)
            node.parent = current
            

if __name__ == '__main__':
    start = time.time()
    # obtain the file from the arguments of execution
    with open(sys.argv[1], 'r') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    students = ast.literal_eval(data)
    openset, closedset, result = astar(getStudents(students))
    end = time.time()

    res = {}
    for s in result.state:
        print(s.id)
        res[s.id + ('C' if s.tr else 'X') + ('R' if s.rm else 'X')] = s.seat

    # output file, with the information of the queue
    fname = "{}-{}".format(os.path.splitext(sys.argv[1])[0], sys.argv[2]) 
    with open(fname + '.output', 'w') as output:
        str = "INITIAL:\t{} \nFINAL:\t{}".format(data, res)
        output.write(str)

    # stat file, with the information of the search
    with open(fname + '.stat', 'w') as stat:
        stat.write("Total time: {}\nPlan cost: {}\nExpanded nodes: {}\nPlan length: {}".format(end-start, result.cost, len(openset), len(closedset)))
