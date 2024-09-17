#!/usr/bin/env pybricks-micropython
from sokoban_new import solve
from move_and_turn import MazeRobot

instructions = solve("worlds/board.txt")
robot = MazeRobot(instructions)
robot._follow_line()
