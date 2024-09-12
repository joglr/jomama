import sys

class TreeNode:
    def __init__(self, state, parent=None, action=None):
        self.state = state
        self.parent = parent
        self.action = action

WALL = "X"
AIR = " "
CAN = "$"
TARGET = "."
ROBOT = "@"
CAN_ON_TARGET = "*"

LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

actions = [LEFT, RIGHT, UP, DOWN]

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


def parse_world(filename):
    with open(filename) as f:
        world = []

        for line in f:
            row = list(line.strip())
            world.append(row)

        return world
    
def addCoordinates(p1, p2):
    p1X, p1Y = p1
    p2X, p2Y = p2

    pXNew = p1X + p2X
    pYNew = p1Y + p2Y

    return(pXNew, pYNew)

def findElementPositions(state, element):
    targetPositions = []
    for row_index, row in enumerate(state):
        for col_index, value in enumerate(row):
            if value == element:
                targetPositions.append((row_index, col_index))
    return targetPositions


def checkIfWithinMap(state, robotPos):
    x, y = robotPos
    if state[x][y] != WALL:
        return True
    return False

def canAndThenWallOrCanAndThenCan(state, robotPos, action):
    nextRobotPos = addCoordinates(robotPos, action)
    currX, currY = robotPos
    nextX, nextY = nextRobotPos
    if state[currX][currY] == CAN:
        if state[nextX][nextY] == CAN | state[nextX][nextX] == WALL:
            return True
    return False

def setPreviousRobotPosition(state, nextRobotPos, action):
    flippedAction = (-action[0], -action[1])
    previousPos = addCoordinates(nextRobotPos, flippedAction)
    prevX, prevY = previousPos
    state[prevX][prevY] = AIR
    return state

def setNewRobotAndCanPosition(state, nextRobotPos, nextCanPositoins):
    robotX, robotY = nextRobotPos
    canX, canY = nextCanPositoins

    state[robotX][robotY] = ROBOT
    state[canX][canY] = CAN

    return state

def setNewRobotPosition(state, nextRobotPos):
    robotX, robotY = nextRobotPos
    state[robotX][robotY] = ROBOT

    return state

def checkIfNextMoveIsCan(state, nextRobotPos):
    robotX, robotY = nextRobotPos
    if state[robotX][robotY] == CAN:
        return True
    return False


def makeMove(state, robotPosition, action):
    nextRobotPosition = addCoordinates(robotPosition, action)
    if checkIfWithinMap(state, nextRobotPosition):
        if not canAndThenWallOrCanAndThenCan(state, nextRobotPosition, action):
            newState = state
            if checkIfNextMoveIsCan(state, nextRobotPosition):
                nextCanPosition = addCoordinates(nextRobotPosition, action)
                newState = setNewRobotAndCanPosition(state, nextRobotPosition, nextCanPosition)
            else:
                newState = setNewRobotPosition(state, nextRobotPosition)

            newState = setPreviousRobotPosition(newState, nextRobotPosition, action)
            return newState
        
    return 
    


def main():
    openQueue = []
    closedList = []

    filename = sys.argv[1]
    initialState = parse_world(filename)

    openQueue.append(initialState)

    robotPosition = findElementPositions(initialState, ROBOT)[0]
    targetPositions = findElementPositions(initialState, TARGET)

    while len(openQueue) > 0:
        currentState = openQueue.pop(0)
        closedList.append(currentState)

        for action in actions:
            newState = makeMove(currentState, robotPosition, action)

            if newState is not None and newState not in closedList:
                canPositions = findElementPositions(newState, CAN)
                if set(targetPositions) == set(canPositions):
                    break
                openQueue.append(newState)
        

if __name__ == "__main__":
    main()

