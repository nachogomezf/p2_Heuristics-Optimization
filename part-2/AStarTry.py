import ast


class Node:
    def __init__(self, seat, rm, trouble):
        self.seat = seat
        self.rm = rm
        self.trouble = trouble
        self.parent = None
    
    def __str__(self):
        return str(self.seat)

initial_state = []
def getGoalState(students):
    res = []
    seat = -1
    troub = False
    dis = False
    for elem in students:
        seat = students[elem]
        if elem[1] == 'C':
            troub = True
        else:
            troub = False
        if elem[2] == 'R':
            dis = True
        else:
            dis = False
        res.append(Node(seat, dis, troub))
    return res

def cost(node):
    if node.parent:
        if node.parent.rm:
            return 0
    else:
        if node.rm:
            return 3
        else:
            return 1

def heuristic(rest):
    res = 0
    for elem in rest:
        res += 1
    return res + 1

def children(node, myset):
    if node is None: return myset
    res = set()
    for elem in myset:
        if elem != node:
            elem.parent = node
            res.add(elem)
    return res


def astar(final_state):
    openset = set()
    for elem in final_state:
        openset.add(elem)
    closedset = set()
    
    while openset:
        current = None
        minC = 1000000
        for elem in openset:
            rest = openset.difference(elem)
            if cost(elem) + heuristic(rest) < minC:
                minC = cost(elem) + heuristic(rest)
                current = elem
        if len(closedset) == len(final_state) - 1:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path
        openset.remove(current)
        closedset.add(current)
        for node in children(current, openset):
            if node in closedset:
                continue
            if current.rm and node.rm:
                continue
            if node not in openset:
                openset.add(node)
            node.parent = current
    raise ValueError('No paths')


if __name__ == '__main__':    
    with open('easytest.prob') as f:
        data = f.read()
    students = ast.literal_eval(data)
    goal = getGoalState(students)
    val = astar(goal)
    print("Hello world")