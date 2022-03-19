from enum import Enum

class Action(Enum):
    Left = 1
    Right = 2
    Up = 3
    Down = 4
    Init = 5

class Location(Enum):
    Empty = 1
    Wall = 2
    Start = 3
    Destination = 4

class Maze:
    def __init__(self, file_name):
        self.mazeMap = []
        i = 0
        with open(file_name, 'r') as file:            
            for lines in file:           
                rowList = []
                                
                for j in range(0, len(lines)-1):                
                    if lines[j] == '1':                        
                        rowList.append(Location.Wall)
                    elif lines[j] == '0':
                        rowList.append(Location.Empty)
                    elif lines[j] == 'S':
                        self.startX = j
                        self.startY = i
                        rowList.append(Location.Start)
                    elif lines[j] == 'E':
                        self.destinationX = j
                        self.destinationY = i                        
                        rowList.append(Location.Destination)                   
                    j = j + 1
                self.mazeMap.append(rowList)
                i = i + 1
    def getLocation(self, coordX, coordY):
        return self.mazeMap[coordY][coordX]
                
class Node:
    def __init__(self, action, location_x, location_y, parent_cost = 0):
        self.action = action
        if(self.action == Action.Init):
            self.x = location_x
            self.y = location_y
            self.path_cost = 0
        else:
            if(self.action == Action.Left):
                self.x = location_x-1
                self.y = location_y                
            elif(self.action == Action.Right):
                self.x = location_x+1
                self.y = location_y
            elif(self.action == Action.Up):
                self.x = location_x
                self.y = location_y-1
            elif(self.action == Action.Down):
                self.x = location_x
                self.y = location_y+1
            self.path_cost = parent_cost+1
    def getParentCoordinates(self):
        if(self.action == Action.Left):
            return (self.x+1, self.y)
        if(self.action == Action.Right):
            return (self.x-1, self.y)
        if(self.action == Action.Up):
            return (self.x, self.y+1)
        if(self.action == Action.Down):
            return (self.x, self.y-1)
        if(self.action == Action.Init):
            return (self.x, self.y)
                    
def breadthFirstSearch(filename):
    maze = Maze(filename)
    initNode = Node(Action.Init, maze.startX, maze.startY)
    frontier = []                # queue
    frontier.append(initNode)
    explored = []
    while(frontier):  # while frontier is not empty
        parentNode = frontier.pop(0)
        #print("X: %d" % parentNode.x)
        #print("Y: %d" % parentNode.y)
        explored.append(parentNode)
        possibleActions =  [Action.Left, Action.Right, Action.Up, Action.Down]
        if(parentNode.action != Action.Init):
            possibleActions.remove(oppositeDirection(parentNode.action))
        for action in possibleActions:
            childNode = Node(action, parentNode.x, parentNode.y, parentNode.path_cost)
            if(maze.mazeMap[childNode.y][childNode.x] == Location.Wall
               or maze.getLocation(childNode.x, childNode.y) == Location.Start):
                continue
            else:
                flag1 = False
                flag2 = False
                for node in frontier:
                    if node.x == childNode.x and node.y == childNode.y:
                        flag1 = True
                for node in explored:
                    if node.x == childNode.x and node.y == childNode.y:
                        flag2 = True
                if(not (flag1 or flag2)):
                    if(maze.getLocation(childNode.x, childNode.y) == Location.Destination): # goal test
                        solution = [] 
                        backTrackNodeCoordX, backTrackNodeCoordY = childNode.getParentCoordinates()
                        while(maze.getLocation(backTrackNodeCoordX, backTrackNodeCoordY) != Location.Start):
                            for exploredNode in explored:
                                if(exploredNode.x == backTrackNodeCoordX and exploredNode.y == backTrackNodeCoordY):
                                    solution.append(exploredNode.action)
                                    backTrackNodeCoordX, backTrackNodeCoordY = exploredNode.getParentCoordinates()
                        return solution
                    frontier.append(childNode)
    return [] # failure

def depthFirstSearch(filename):
    maze = Maze(filename)
    initNode = Node(Action.Init, maze.startX, maze.startY)
    stack = []                # queue
    stack.append(initNode)
    explored = []
    while(stack):
        parentNode = stack.pop()
        #print("X: %d" % parentNode.x)
        #print("Y: %d" % parentNode.y)
        flag1 = False
        flag2 = False
        for node in stack:
            if node.x == parentNode.x and node.y == parentNode.y:
                flag1 = True
        for node in explored:
            if node.x == parentNode.x and node.y == parentNode.y:
                flag2 = True
        if(not (flag1 or flag2)):
            if(maze.getLocation(parentNode.x, parentNode.y) == Location.Destination): # goal test
                print(parentNode.path_cost)
                solution = [] 
                backTrackNodeCoordX, backTrackNodeCoordY = parentNode.getParentCoordinates()
                while(maze.getLocation(backTrackNodeCoordX, backTrackNodeCoordY) != Location.Start):
                    for exploredNode in explored:
                        if(exploredNode.x == backTrackNodeCoordX and exploredNode.y == backTrackNodeCoordY):
                            solution.append(exploredNode.action)
                            backTrackNodeCoordX, backTrackNodeCoordY = exploredNode.getParentCoordinates()                
                return solution
            explored.append(parentNode)
            possibleActions =  [Action.Left, Action.Right, Action.Up, Action.Down]
            if(parentNode.action != Action.Init):
                possibleActions.remove(oppositeDirection(parentNode.action))
            for action in possibleActions:
                childNode = Node(action, parentNode.x, parentNode.y, parentNode.path_cost)
                if(maze.mazeMap[childNode.y][childNode.x] == Location.Wall
                   or maze.getLocation(childNode.x, childNode.y) == Location.Start):
                    continue
                else:
                    stack.append(childNode)
    return []
            
class DLSResult(Enum):
    Cutoff = 1
    Failure = 2
    Success = 3
# recursive DLS
# input: maze, explored (initially empty), node, limit,
# output: explored, (cuttoff, success, or failure)

def oppositeDirection(direction):
    if direction == Action.Left:
        return Action.Right;
    elif direction == Action.Right:
        return Action.Left
    elif direction == Action.Up:
        return Action.Down
    elif direction == Action.Down:
        return Action.Up

def recursiveDLS(maze, node, limit, explored):
    if(maze.getLocation(node.x, node.y) == Location.Destination):  # is Solution
        return explored, node, DLSResult.Success
    elif limit == 0: return explored, node, DLSResult.Cutoff
    else:
        cutoff_occured = False
        possibleActions = [Action.Left, Action.Right, Action.Up, Action.Down]
        if(node.action != Action.Init):
            possibleActions.remove(oppositeDirection(node.action))
        for action in possibleActions:         
            childNode = Node(action, node.x, node.y, node.path_cost)
            exploredFlag = False
            if(maze.mazeMap[childNode.y][childNode.x] == Location.Wall
               or maze.getLocation(childNode.x, childNode.y) == Location.Start):
                continue                
            for exploredNode in explored:
                if(exploredNode.x == childNode.x and exploredNode.y == childNode.y):
                    exploredFlag = True
            if(exploredFlag): continue
           
            explored.append(childNode)    # add childNode to epxlored
            explored, destinationNode, result = recursiveDLS(maze, childNode, limit-1, explored)
            if result == DLSResult.Cutoff: cutoff_occured = True
            elif result != DLSResult.Failure: return explored, destinationNode, result
        if(cutoff_occured): return explored, node, DLSResult.Cutoff
        else: return explored, node, DLSResult.Failure

def depthLimitedSearch(filename, limit):
    maze = Maze(filename)
    initNode = Node(Action.Init, maze.startX, maze.startY)
    explored, destinationNode, result = recursiveDLS(maze, initNode, limit, [])
    if(result == DLSResult.Cutoff):
        print("Cutoff reached")
        return []
    elif(result == DLSResult.Failure):
        print("No solutions")
        return []
    elif(result == DLSResult.Success):
        solution = [] 
        backTrackNodeCoordX, backTrackNodeCoordY = destinationNode.getParentCoordinates()
        while(maze.getLocation(backTrackNodeCoordX, backTrackNodeCoordY) != Location.Start):
            for exploredNode in explored:
                if(exploredNode.x == backTrackNodeCoordX and exploredNode.y == backTrackNodeCoordY):
                    solution.append(exploredNode.action)
                    backTrackNodeCoordX, backTrackNodeCoordY = exploredNode.getParentCoordinates()                
        return solution
def printSolution(solution):
    if(solution == []): return
    print("Start->", end='')
    for step in reversed(solution):
        if(step == Action.Left):
            print("Left->", end='')
        if(step == Action.Right):
            print("Right->", end='')
        if(step == Action.Up):
            print("Up->", end='')
        if(step == Action.Down):
            print("Down->", end='')
    print("Destination")

def main():
    solution1 = breadthFirstSearch(r'C:\users\jimmy\Desktop\aicourse\MazeData.txt')
    print(len(solution1))
    print("Breadth First Search")
    printSolution(solution1)
    solution2 = depthFirstSearch(r'C:\users\jimmy\Desktop\aicourse\MazeData.txt')
    print("Depth First Search")    
    print(len(solution2))
    printSolution(solution2)
    print("Depth Limited Search")     
    solution3 = depthLimitedSearch(r'C:\users\jimmy\Desktop\aicourse\MazeData.txt', 78)
    printSolution(solution3)
main()
