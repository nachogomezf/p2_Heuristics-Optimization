import ast

inf = float('inf')

class Node:
    def __init__(self, student, seat):
        self.id =  student[:-2]
        self.disabled = True if student[-1] == 'R' else False
        self.troubled = True if student[-2] == 'C' else False
        self.seat = seat
        self.parent = None
        self.H = 0
        self.G = -inf
    
    def cost(self,other):
        return 3 if self.disabled else 1
        
def children(node, students):
    if node is None: return students #base case
    result = []
    for st1 in students:
        #If the student isn't the current one, add it to the children list
        if st1.id != node.id: 
            st1.parent = node
            result.append(st1)
    return result

    

def check_goal(current, closedset, students):
    if current.id in [o.id for o in closedset]: return False
    return True if (len(students) == (1+len(closedset))) else False

def addStudents(students):
    res = []
    for st, seat in students.items():
        res.append(
            Node(st, seat)
        )
    return res

def currentQueueLength(current):
    path = []
    while current.parent:
        path.append(current)
        current = current.parent
    return len(path)

def aStar(students):
    #The open and closed sets
    openset = set()
    closedset = set()
    #Get all the students as operators
    current = children(None, students)
    #Add the starting node to the open set by selecting the one with lesser cost
    for st in current:
        openset.add(st)
    #While the open set is not empty
    while openset:
        #Find the item in the open set with the lowest G + H score
        current = min(openset, key=lambda o:o.G + o.H)
        #If it is the item we want, retrace the path and return it
        if currentQueueLength(current) == len(students)-1:
            path = []
            while current.parent:
                path.append(current)
                current = current.parent
            path.append(current)
            return path[::-1]
        #Remove the item from the open set
        openset.remove(current)
        #Add it to the closed set
        closedset.add(current)
        #Loop through the node's children
        for node in children(current, students):
            #If it is already in the closed set, skip it
            if node in closedset:
                continue
            #We cannot have two successive disabled people
            if current.disabled and node.disabled:
                continue
            #Falta checkear si es disabled y es el ultimo
            #Otherwise if it is already in the open set
            if node in openset:
                #Check if we beat the G score 
                new_g = current.G + current.cost(node)
                if node.G >= new_g:
                    #If so, update the node to have a new parent
                    node.G = new_g
                    node.parent = current
            else:
                #If it isn't in the open set, calculate the G and H score for the node
                node.G = current.G + current.move_cost(node)
                # TODO : comprobar heuristica es admisible
                node.H = len(students) - len(closedset)
                #Set the parent to our current item
                node.parent = current
                #Add it to the set
                openset.add(node)
    #Throw an exception if there is no path

    #Guardar en una lista/dict los estudiantes problematicos ya asignados y su asiento
    raise ValueError('No Path Found')


if __name__ == "__main__":

    with open('easytest.prob') as f:
        data = f.read()
    # reconstructing the data as a dictionary
    students = ast.literal_eval(data)
    result = aStar(addStudents(students))
    print(result)