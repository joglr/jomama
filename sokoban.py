import sys

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

def find_pois(world):
    robot_pos = None
    target_pos = None
    can_pos = None

    y = 0
    for row in world:
        if ROBOT in row:
            robot_pos = (row.index(ROBOT), y)

        if TARGET in row:
            target_pos = (row.index(TARGET), y)

        if CAN in row:
            can_pos = (row.index(CAN), y)

        y += 1

    return robot_pos, target_pos, can_pos

def parse_world(filename):
    with open(filename) as f:
        world = []

        for line in f:
            row = list(line.strip())
            world.append(row)

        return world


# Moving the robot

# Tree search of moves that the cans can make
# Weights: Distance the robot needs to move to push the box in a given direction

# rx, ry = robot


def bfs_push(world, can, target):
    visited = set([can])
    parent_map = {can: None}
    queue = [can]

    # Queue the movements that the cans can make

    i = 0
    while len(queue) > 0:
        pos = queue.pop(0)

        if pos == target:
            print("🥫 found can target")
            # Return backtracked list of pushes that neees to be performed
            path = [pos]
            current_pos = pos

            i = 0

            while parent_map[current_pos] is not None:
                parent = parent_map[current_pos]
                path.append(parent)
                parent_pos = parent["pos"]
                current_pos = parent_pos
                i += 1
                if i > 1_000_000:
                    print("💩 gave up")
                    break

            return list(reversed(path))

        left = add(pos, LEFT)
        right = add(pos, RIGHT)
        up = add(pos, UP)
        down = add(pos, DOWN)

        if is_free(world, left) and is_free(world, right) and left not in visited:
            parent_map[left] = {"pos": pos, "robot": right, "push": LEFT}
            visited.add(left)
            queue.append(left)

        if is_free(world, right) and is_free(world, left) and right not in visited:
            parent_map[right] = {"pos": pos, "robot": left, "push": RIGHT}
            visited.add(right)
            queue.append(right)

        if is_free(world, up) and is_free(world, down) and up not in visited:
            parent_map[up] = {"pos": pos, "robot": down, "push": UP}
            visited.add(up)
            queue.append(up)

        if is_free(world, down) and is_free(world, up) and down not in visited:
            parent_map[down] = {"pos": pos, "robot": up, "push": DOWN}
            visited.add(down)
            queue.append(down)

        i += 1


def bfs_navigate(world, robot_pos, target_pos):
    visited = set([robot_pos])
    parent_map = {robot_pos: None}
    queue = [robot_pos]

    # Queue the movements that the cans can make

    i = 0
    while len(queue) > 0:
        pos = queue.pop(0)
        # print(f"{pos = }")
        # print(f"{queue = }")

        if pos == target_pos:
            print("🎖️ found robot push position")
            # Return backtracked list of pushes that neees to be performed
            path = [pos]
            current_pos = pos

            i = 0

            while parent_map[current_pos] is not None:
                if "pos" not in parent_map[current_pos]:
                    break
                parent = parent_map[current_pos]
                path.append(parent)
                parent_pos = parent["pos"]
                current_pos = parent_pos
                i += 1
                if i > 1_000_000:
                    print("💩 gave up")
                    break

            return list(reversed(path))

        left = add(pos, LEFT)
        right = add(pos, RIGHT)
        up = add(pos, UP)
        down = add(pos, DOWN)

        # print(f"{left = }")
        # print(f"{right = }")
        # print(f"{up = }")
        # print(f"{down = }")

        if is_free(world, left) and left not in visited:
            # print("can be pushed left from " + str(pos))
            parent_map[left] = {"pos": pos, "dir": LEFT}
            visited.add(left)
            queue.append(left)

        if is_free(world, right) and right not in visited:
            # print("can be pushed right from " + str(pos))
            parent_map[right] = {"pos": pos, "dir": RIGHT}
            visited.add(right)
            queue.append(right)

        if is_free(world, up) and up not in visited:
            # print("can be pushed up from " + str(pos))
            parent_map[up] = {"pos": pos, "dir": UP}
            visited.add(up)
            queue.append(up)

        if is_free(world, down) and down not in visited:
            # print("can be pushed down from " + str(pos))
            parent_map[down] = {"pos": pos, "dir": DOWN}
            visited.add(down)
            queue.append(down)

        # print("____ queue   ____")
        # print_world(world, queue)
        # print("____ visited ____")
        # print_world(world, visited)
        i += 1


def print_world(world, visited):
    char_map = {
        AIR: " ",
        WALL: "+",
        CAN: "C",
        TARGET: "T",
        ROBOT: "R",
        CAN_ON_TARGET: "*",
    }
    print()
    for y, row in enumerate(world):
        for x, spot in enumerate(row):
            if (x, y) in visited:
                print(str(list(visited).index((x, y))) + " ", end="")
            else:
                print(char_map[spot] + " ", end="")
        print()
    print()


def is_free(world, pos):
    x, y = pos

    spot = None

    try:
        spot = world[y][x]
    except IndexError:
        return False

    spot_is_free = spot == AIR or spot == ROBOT or spot == TARGET

    return spot_is_free


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def update_world(world, can_pos, robot_pos):
    robot_pos, target_pos, can_pos = find_pois(world=world)

    old_rx, old_ry = robot_pos
    old_cx, old_cy = can_pos

    world[old_ry][old_rx] = AIR
    world[old_cy][old_cx] = AIR

    cx, cy = can_pos
    rx, ry = robot_pos

    world[cy][cx] = CAN
    world[ry][rx] = ROBOT

    return world

def main():
    filename = sys.argv[1]
    world = parse_world(filename)
    current_robot_pos, target_pos, can_pos = find_pois(world)

    push_path = bfs_push(world, can_pos, target_pos)
    print(f"{push_path = }")
    print(f"{len(push_path) = }")

    for push_step in push_path:
        print(f"{push_step = }")
        can_pos = push_step["pos"]
        robot_push_pos = push_step["robot"]
        push_direction = push_step["push"]

        # 1. Navigate the robot to the can
        robot_path = bfs_navigate(world=world, robot_pos=current_robot_pos, target_pos=robot_push_pos)
        print(f"{robot_path = }")

        # TODO: Implement the robot movement
        # TODO: Turn the robot to the right direction and move until next intersection

        # 2. TODO: Push the can



        # 3. Update the world
        world = update_world(world=world, can_pos=add(can_pos, push_direction), robot_pos=can_pos)

if __name__ == "__main__":
    main()
