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


def read_world_and_find_pois(filename):
    robot_pos = None
    target_pos = None
    can_pos = None

    with open(filename) as f:
        world = []
        y = 0
        for line in f:
            row = list(line.strip())
            if ROBOT in row:
                robot_pos = (row.index(ROBOT), len(world))

            if TARGET in row:
                target_pos = (row.index(TARGET), len(world))

            if CAN in row:
                can_pos = (row.index(CAN), len(world))

            world.append(row)
            y += 1
        return world, robot_pos, target_pos, can_pos


# Moving the robot

# Tree search of moves that the cans can make
# Weights: Distance the robot needs to move to push the box in a given direction

# rx, ry = robot


def bfs_push(world, can, target):
    cx, cy = can
    tx, ty = target

    visited = set([can])
    parent_map = {can: None}
    queue = [can]

    # Queue the movements that the cans can make

    i = 0
    while len(queue) > 0:
        pos = queue.pop(0)
        print(f"{pos = }")
        print(f"{queue = }")

        if pos == target:
            print("🎖️ found target")
            # Return backtracked list of pushes that neees to be performed
            path = [pos]
            current_pos = pos

            i = 0

            print(parent_map)

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

        print(f"{left = }")
        print(f"{right = }")
        print(f"{up = }")
        print(f"{down = }")

        if is_free(world, left) and is_free(world, right) and left not in visited:
            print("can be pushed left from " + str(pos))
            parent_map[left] = {"pos": pos, "robot": right, "push": LEFT}
            visited.add(left)
            queue.append(left)

        if is_free(world, right) and is_free(world, left) and right not in visited:
            print("can be pushed right from " + str(pos))
            parent_map[right] = {"pos": pos, "robot": left, "push": RIGHT}
            visited.add(right)
            queue.append(right)

        if is_free(world, up) and is_free(world, down) and up not in visited:
            print("can be pushed up from " + str(pos))
            parent_map[up] = {"pos": pos, "robot": down, "push": UP}
            visited.add(up)
            queue.append(up)

        if is_free(world, down) and is_free(world, up) and down not in visited:
            print("can be pushed down from " + str(pos))
            parent_map[down] = {"pos": pos, "robot": up, "push": DOWN}
            visited.add(down)
            queue.append(down)

        print("____ queue   ____")
        print_world(world, queue)
        print("____ visited ____")
        print_world(world, visited)
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


def main():
    filename = sys.argv[1]
    world, robot_pos, target_pos, can_pos = read_world_and_find_pois(filename)

    path = bfs_push(world, can_pos, target_pos)
    print("path:", path)


if __name__ == "__main__":
    main()
