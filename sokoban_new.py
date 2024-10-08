import copy
import sys

class TreeNode:
    def __init__(self, state, parent=None, action=None, orientation=None):
        self.state = state
        self.parent = parent
        self.action = action

WALL = "X"
AIR = " "
CAN = "$"
TARGET = "."
ROBOT = "@"
CAN_ON_TARGET = "*"

'''
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)
'''
LEFT = (0, -1)
RIGHT = (0, 1)
UP = (-1, 0)
DOWN = (1, 0)

ORIENTATION_U = 12
ORIENTATION_D = 6
ORIENTATION_L = 9
ORIENTATION_R = 3


actions = [LEFT, RIGHT, UP, DOWN]

def parse_world(filename):
    with open(filename) as f:
        world = []

        for line in f:
            row = list(line.strip())
            world.append(row)

        return world


def parse_world_competition_format(filename):

    with open(filename) as f:
        world = []

        for line in f:
            row = list(line.strip())
            world.append(row)

    indices_to_remove = {2, 4, 6}

    new_world = []

    for i in range(len(world)):
        if i in indices_to_remove:
            continue
        new_world.append([])
        for j in range(len(world[i])):
            if j in indices_to_remove:
                continue
            new_world[-1].append(world[i][j])

    # for i in range(len(new_world)):
    #     new_world[i] = ''.join(new_world[i])
    
    return new_world

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
            elif value == CAN_ON_TARGET and (element == CAN or element == TARGET):
                targetPositions.append((row_index, col_index))
    return targetPositions


def checkIfWithinMap(state, robotPos):
    x, y = robotPos
    if state[x][y] != WALL:
        return True
    return False

def canAndThenWallOrCanAndThenCan(currentState, robotPos, action):
    nextRobotPos = addCoordinates(robotPos, action)
    currX, currY = robotPos
    nextX, nextY = nextRobotPos
    if currentState[currX][currY] == CAN or currentState[currX][currY] == CAN_ON_TARGET:
        if currentState[nextX][nextY] == CAN or currentState[nextX][nextY] == WALL or currentState[nextX][nextY] == CAN_ON_TARGET:
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
    if state[robotX][robotY] == CAN or state[robotX][robotY] == CAN_ON_TARGET:
        return True
    return False


def makeMove(currentState, robotPosition, action):
    nextMoveIsCan = False
    nextRobotPosition = addCoordinates(robotPosition, action)
    if checkIfWithinMap(currentState, nextRobotPosition):
        if not canAndThenWallOrCanAndThenCan(currentState, nextRobotPosition, action):
            nextState = copy.deepcopy(currentState)
            if checkIfNextMoveIsCan(currentState, nextRobotPosition):
                nextMoveIsCan = True
                nextCanPosition = addCoordinates(nextRobotPosition, action)
                nextState = setNewRobotAndCanPosition(nextState, nextRobotPosition, nextCanPosition)
            else:
                nextState = setNewRobotPosition(nextState, nextRobotPosition)

            nextState = setPreviousRobotPosition(nextState, nextRobotPosition, action)
            return [nextState, nextMoveIsCan]

    return

def reconstruct_path(node):
    path = []
    while node.parent is not None:
        path.append(node.action)
        node = node.parent
    path.reverse()
    return path


orientations = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # [Up, Right, Down, Left]

# Helper function to get the new orientation after turning
def turn_robot(current_orientation, turn_direction):
    idx = orientations.index(current_orientation)
    if turn_direction == "left":
        idx = (idx - 1) % 4  # Turning left means moving counterclockwise
    elif turn_direction == "right":
        idx = (idx + 1) % 4  # Turning right means moving clockwise
    return orientations[idx]

def flattenSteps(steps):
    flattened = []
    for step in steps:
        if isinstance(step, tuple) and len(step) == 2:  # Check if it's a tuple of size 2 (normal move)
            flattened.append(step)
        elif isinstance(step, (list, tuple)) and len(step) in [3, 4]:  # Check if it's a triplet or fourplet
            flattened.extend(flattenSteps(step))  # Recursively flatten triplets or fourplets
    return flattened


def convertCoordinatesIntoInstructions(path):
    instructions = []
    for step in path:
        if step == LEFT:
            instructions.append("left")
        elif step == RIGHT:
            instructions.append("right")
        elif step == UP:
            instructions.append("up")
        elif step == DOWN:
            instructions.append("down")
    return instructions

def stateToHashable(state):
    return tuple(tuple(row) for row in state)

def mergeTripletsIfSame(arr):
    i = 0
    result = []
    
    while i < len(arr):
        current = arr[i]
        
        # Check if the current element and the next one are triplets
        if isinstance(current, tuple) and len(current) == 3 and i + 1 < len(arr):
            next_elem = arr[i + 1]
            
            # Check if the next element is also a triplet and contents are identical
            if isinstance(next_elem, tuple) and len(next_elem) == 3:
                if current == next_elem:
                    # Merge the two triplets into a fourplet
                    fourplet = (current[0], current[0], next_elem[0], current[2])
                    result.append(fourplet)
                    # Skip the next triplet since it's merged
                    i += 2
                    continue
        
        # If not a triplet or no merging, append the current element as is
        result.append(current)
        i += 1
    
    return result


def solve(filename=None, competition_format=False):
    openQueue = []
    closedSet = set()

    if filename is None:
        try:
            filename = sys.argv[1]
        except IndexError:
            pass

    if filename is None:
        filename = "worlds/board.txt"

    if competition_format:
        initialState = parse_world_competition_format(filename)
    else:
        initialState = parse_world(filename)

    # Create the root node (initial state) with no parent and no action
    root = TreeNode(state=initialState)
    openQueue.append(root)

    targetPositions = findElementPositions(initialState, TARGET)

    solutionFound = False
    solutionNode = None

    while len(openQueue) > 0:
        currentNode = openQueue.pop(0)
        currentState = currentNode.state

        closedSet.add(stateToHashable(currentState))

        robotPosition = findElementPositions(currentState, ROBOT)[0]

        for action in actions:
            result = makeMove(currentState, robotPosition, action)
            if result is not None:
                newState, nextMoveIsCan = result
                if nextMoveIsCan == True:
                    action = (action, action, (-action[0], -action[1]))
            else:
                newState = result
            if newState is not None and stateToHashable(newState) not in closedSet:
                newNode = TreeNode(state=newState, parent=currentNode, action=action)

                canPositions = findElementPositions(newState, CAN)
                if set(targetPositions) == set(canPositions):
                    solutionNode = newNode
                    solutionFound = True
                    break

                openQueue.append(newNode)
        if solutionFound:
            break

    if solutionFound and solutionNode:
        # Reconstruct the path by backtracking from the solution node
        path = reconstruct_path(solutionNode)
        simplePath = mergeTripletsIfSame(path)
        flattenPath = flattenSteps(simplePath)
        #print(flattenPath)
        instructions = convertCoordinatesIntoInstructions(flattenPath)
        instructions.pop()  # Removes the last element
        print(instructions)
        #print("Solution path (actions):", path)
        print("Final state:")
        for row in solutionNode.state:
            print(''.join(row))

        return instructions
    else:
        print("No solution found")
        return None

if __name__ == "__main__":
    solve()

